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
        if not hasattr(instance, "parents") or (hasattr(instance, "parents") and instance.parents.all().count() is 0):
            with transaction.atomic():
                # Only update the hierarchy FIELD related to this instance's app_type: HD or PRO
                # Also ignore sub categories - cats with parent field
                hierarchy_max = self.filter(
                    app_type=instance.app_type,
                    parents__isnull=True,
                ).aggregate(Max('hierarchy')).get('hierarchy__max') or 0
                instance.hierarchy = hierarchy_max + 1
                instance.save()
                return instance

    def move(self, obj, old_pos, new_pos, app_type, save=True):
        """Insert at position in the hierarchy and adjust the
        rest of the search categories' hierarchies, so they're  in sequence.

        For example:
          apples = SearchCategory.objects.get(name="apples")
          SearchCategories.objects.move(apples, 5)

        :param obj: SearchCategory to move.
        :param old_pos: Hierarchy moving from.
        :param new_pos: Hierarchy number to move to.
        :param app_type: The app specific SC to change, either hd or pro
        :param save: Optionally disable the save, so this can be called in the pre save.
        """
        # Filter out categories that are sub categories
        all_categories = self.get_queryset()
        not_sub_categories_id = []
        for category in all_categories:
            if not hasattr(category, "parents") or (hasattr(category, "parents") and category.parents.all().count() is 0):
                not_sub_categories_id.append(category.id)

        qs = all_categories.filter(id__in=not_sub_categories_id)
        with transaction.atomic():
            temp_new_pos = int('99999' if new_pos is None else new_pos)
            temp_old_pos = int('99999' if old_pos is None else old_pos)
            if temp_old_pos > temp_new_pos:
                qs.filter(app_type=app_type, hierarchy__lt=temp_old_pos, hierarchy__gte=temp_new_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') + 1,
                    synchronised=False
                )
            elif temp_old_pos < temp_new_pos:
                qs.filter(app_type=app_type, hierarchy__lte=temp_new_pos, hierarchy__gt=temp_old_pos).exclude(pk=obj.pk).update(
                    hierarchy=F('hierarchy') - 1,
                    synchronised=False
                )
            if temp_new_pos == 0:
                new_pos = 1
            obj.hierarchy = new_pos
            if save:
                obj.save()
