from queue import Queue
from threading import Thread
from multiprocessing import cpu_count

from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator

from idcops.models import Device


class Command(BaseCommand):
    help = "更新所有设备的高度(U)、U位范围"

    batch_size = 256

    # max_thread = (100 * cpu_count())

    def add_arguments(self, parser):
        parser.add_argument(
            '--size', type=int, action='store',
            dest='size', default=self.batch_size,
            help=f"指定每个线程处理多少条设备信息，默认是: {self.batch_size}/thread",
        )

    def fix_device_height(self, obj):
        # 主要业务逻辑
        height = obj.units.all().count()
        Device.objects.filter(pk=obj.pk).update(height=height)
        Device.objects.filter(pk=obj.pk).update(urange=obj.list_units())

    def handle(self, *args, **options):
        per_page = options['size']
        objects = Device.objects.filter()
        page = Paginator(objects, per_page=per_page)
        object_list = page.object_list
        try:
            if object_list.exists():
                q = Queue()

                def worker():
                    while True:
                        if q.empty():
                            return
                        else:
                            item = q.get()
                            self.fix_device_height(item)
                            q.task_done()
                for obj in object_list:
                    q.put(obj)
                threads = list()
                [
                    threads.append(Thread(target=worker, daemon=True))
                    for _ in range(page.num_pages)
                ]
                [t.start() for t in threads]
                [t.join() for t in threads]
                print(
                    f"threads number: {len(threads)} ({per_page}/thread), total: {page.count}"
                )
            else:
                print('No objects')
        except CommandError as e:
            raise(e)
