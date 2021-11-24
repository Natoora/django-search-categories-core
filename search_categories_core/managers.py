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
            hierarchy_field_str = 'hierarchy_' + instance.app_type.lower()
            hierarchy_max_str = hierarchy_field_str + '__max'
            hierarchy_max = self.aggregate(Max(hierarchy_field_str)).get(hierarchy_max_str) or 0
            new_hierarchy = hierarchy_max + 1
            setattr(instance, hierarchy_field_str, new_hierarchy)
            instance.save()
            return instance

    def move(self, obj, old_pos, new_pos, field, save=True):
        """Insert at position in the hierarchy and adjust the
        rest of the search categories' hierarchies so they're  in sequence.

        For example:
          apples = SearchCategory.objects.get(name="apples")
          SearchCategories.objects.move(apples, 5)

        :param obj: SearchCategory to move.
        :param old_pos: Hierarchy moving from.
        :param new_pos: Hierarchy number to move to.
        :param field: The hierarchy model field to update, either hierarchy_hd or hierarchy_pro
        :param save: Optionally disable the save, so this can be called in the pre save.
        """
        qs = self.get_queryset()
        with transaction.atomic():
            if old_pos > int(new_pos):
                qs = qs.filter(**{(field+'__lt'): old_pos, (field+'__gte'): new_pos}).exclude(pk=obj.pk)
                print(qs)
                qs.update(
                    **{field: F(field) + 1}
                )
            elif old_pos < int(new_pos):
                qs = qs.filter(**{(field+'__lte'): new_pos, (field+'__gt'): old_pos}).exclude(pk=obj.pk)
                print(qs)
                qs.update(
                    **{field: F(field) - 1}
                )
            obj.hierarchy = new_pos
            if save:
                obj.save()
