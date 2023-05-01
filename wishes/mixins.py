from wishes.models import WishList


class GetCurrentWishMixin:
    def get_object(self):
        return WishList.objects.get_or_create(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )[0]
