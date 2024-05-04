# from django_cron import CronJobBase, Schedule
# from .models import User, Bag
# from django.utils import timezone
# from datetime import datetime
#
#
# class UpdateFanStatus(CronJobBas):
#     RUN_EVERY_MIN = 59
#
#     scheduler = Schedule(run_every_min=RUN_EVERY_MIN)
#     code = 'user.update_fan_status'
#
#     def do:
#         users = User.objects.filter(is_active=True, fans__isnull=False).exclude(fans='')
#         for user in users:
#             fan_list = user.fans.split('@')[1:]
#             for item in fan_list:
#                 fan = item.split('~')
#                 fan_id =  fan[0]
#                 time_register = datetime.strptime(fan[1], "%Y-%m-%d %H:%M:%S").day
#
#                 if (timezone.now() - time_register) >= 30:
#                     fan = User.objects.get(user_id=fan_id)
#                     fan_bag = Bag.objects.get(user=fan)
#                     if fan_bag.sapphires >= 25:
#                         fan_bag.sapphires -= 25
#                         fan_bag.save()
#                         user.fans = user.fans.replace(item, (fan + '~' + str(timezone.now())))
#                         user.save()
#                         user_bag = Bag.objects.get(user=user)
#                         user_bag.sapphires += 20
#                         user_bag.save()
#                     else:
#                         split_list = user.fans.split(item)
#                         user.fans = ''.join(split_list)
#                         user.save()
