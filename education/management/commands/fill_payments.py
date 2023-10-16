from django.core.management import BaseCommand

from education.models import Payments, Lesson, Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        paymants_list = [
            {'lesson': 1, 'payment_sum': 3000, 'payment_method': 'cash'},
            {'course': 2, 'payment_sum': 3000, 'payment_method': 'card'},
            {'course': 2, 'payment_sum': 3000, 'payment_method': 'card'},
            {'lesson': 1, 'payment_sum': 3000, 'payment_method': 'card'},
            {'lesson': 1, 'payment_sum': 3000, 'payment_method': 'cash'}
        ]

        payments_for_create = []
        for payments_item in paymants_list:
            if payments_item.get("lesson"):
                lesson_id = payments_item.pop('lesson')
                lesson = Lesson.objects.get(id=lesson_id)
                payments_item['lesson'] = lesson
            else:
                course_id = payments_item.pop('course')
                course = Course.objects.get(id=course_id)
                payments_item['course'] = course
            payments_for_create.append(
                Payments(**payments_item)
            )
        #print(payments_for_create)
        Payments.objects.bulk_create(payments_for_create)



    # products_for_create = []
    # for product_item in product_list:
    #   category_id = product_item.pop('category_id')
    #   category = Category.objects.get(id=category_id)
    #   product_item['category'] = category
    #   products_for_create.append(
    #     Product(**product_item)
    #   )
    #
    # Product.objects.bulk_create(products_for_create)