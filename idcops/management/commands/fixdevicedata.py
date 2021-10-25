from django.core.management.base import BaseCommand, CommandError

from idcops.models import Device
from idcops.lib.tasks import device_post_save


class Command(BaseCommand):
    help = "更新所有设备的高度(U)、状态、U位范围数据"

    def handle(self, *args, **options):
        try:
            devices = Device.objects.filter()
            if devices.exists():
                for device in devices:
                    device_post_save(device.pk)
        except Exception as e:
            raise CommandError(e)
