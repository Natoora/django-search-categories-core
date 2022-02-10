from django.db import models, transaction
from django.db.models import F, Max


class SearchCategoryManager(models.Manager):
    """
    SearchCategory model manager.
    """

    def create(self, *args, **kwargs):
        """
        When creating a SearchCategory
        Populate the hierarchy field with the max hierarchy + 1.
        BUT taking into account the SC APP_TYPE too
        """
        instance = self.model(**kwargs)
        with transaction.atomic():
            # Only update the hierarchy FIELD related to this instance's app_type: HD or PRO
            hierarchy_max = self.filter(app_type=instance.app_type).aggregate(Max('hierarchy')).get('hierarchy__max') or 0
            instance.hierarchy = hierarchy_max + 1
            instance.save()
            return instance

    def move(self, obj, old_pos, new_pos, app_type, save=True):
        """Insert at position in the hierarchy and adjust the
        rest of the search categories' hierarchies so they're  in sequence.

        For example:
          apples = SearchCategory.objects.get(name="apples")
          SearchCategories.objects.move(apples, 5)

        :param obj: SearchCategory to move.
        :param old_pos: Hierarchy moving from.
        :param new_pos: Hierarchy number to move to.
        :param app_type: The app specific SC to change, either hd or pro
        :param save: Optionally disable the save, so this can be called in the pre save.
        """
        qs = self.get_queryset()
        qs.filter(app_type=app_type)
        with transaction.atomic():
            temp_new_pos = int('99999' if new_pos is None else new_pos)
            temp_old_pos = int('99999' if old_pos is None else old_pos)
            if temp_old_pos > temp_new_pos:
                qs.filter(hierarchy__lt=temp_old_pos, hierarchy__gte=temp_new_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') + 1,
                    synchronised=False
                )
            elif temp_old_pos < temp_new_pos:
                qs.filter(hierarchy__lte=temp_new_pos, hierarchy__gt=temp_old_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') - 1,
                    synchronised=False
                )
            if temp_new_pos == 0:
                new_pos = 1
            obj.hierarchy = new_pos
            if save:
                obj.save()
