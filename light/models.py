from django.db import models
from datetime import datetime, time


class Registry(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)


class Config(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    on_time_at = models.DateTimeField(blank=False, null=False)
    off_time_at = models.DateTimeField(blank=False, null=False)


class Controller(models.Model):
    tag = models.CharField(unique=True, null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    light_signal = models.BooleanField(blank=False, null=False)


class Light:

    def __init__(self):
        self.on_time_at: time
        self.off_time_at: time

    @staticmethod
    def get_controller_updated_datetime(tag: str) -> datetime:
        return Config.objects.get(tag=tag).__dict__['updated_at']

    @staticmethod
    def is_tag_in_registry(tag: str) -> bool:
        if len(Registry.objects.filter(tag=tag)):
            return True
        else:
            return False

    @staticmethod
    def add_tag_in_registry(tag) -> bool:
        v, c = Registry.objects.update_or_create(tag=tag)
        return c

    @staticmethod
    def update_config(
            tag: str,
            on_time_at: time,
            off_time_at: time,
    ):
        Config.objects.update_or_create(
            tag=tag,
            defaults={
                "on_time_at": on_time_at,
                "off_time_at": off_time_at
            }
        )
        return True

    def get_config(self, tag: str):
        _ = Config.objects.get(tag=tag).__dict__
        self.on_time_at = _['on_time_at']
        self.off_time_at = _['off_time_at']
        return _

    @staticmethod
    def update_controller(
            tag: str,
            light_signal: bool):
        Controller.objects.update_or_create(
            tag=tag,
            defaults={
                "light_signal": light_signal,
            }
        )
