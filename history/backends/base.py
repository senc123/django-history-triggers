import uuid

from django.apps import apps
from django.db import models
from django.db.backends.utils import split_identifier, truncate_name
from django.utils import timezone

from history import conf, get_history_model
from history.models import AbstractObjectHistory


class HistorySession:
    def __init__(self, backend, **fields):
        self.backend = backend
        self.fields = {}
        # Sanitize based on session fields in the object history model.
        for field in backend.session_fields():
            value = fields.get(field.name)
            if isinstance(value, models.Model):
                value = value.pk
            if value is not None:
                self.fields[field.name] = value
        self.fields.setdefault("session_id", str(uuid.uuid4()))
        self.fields.setdefault("session_date", timezone.now().isoformat())

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc_details):
        self.stop()


class HistoryBackend:
    session_class = HistorySession

    def __init__(self, connection):
        self.conn = connection

    def install(self):
        pass

    def remove(self):
        pass

    def get_models(self):
        return [
            model
            for model in apps.get_models(include_auto_created=True)
            if not issubclass(model, AbstractObjectHistory)
            and model._meta.app_label not in conf.IGNORE_APPS
        ]

    def session_fields(self):
        HistoryModel = get_history_model()
        auto_populated = [
            "id",
            "change_type",
            "content_type",
            "object_id",
            "snapshot",
            "changes",
        ]
        for f in HistoryModel._meta.get_fields():
            if f.concrete and f.name not in auto_populated:
                yield f

    def execute(self, sql, params=None, fetch=False):
        with self.conn.cursor() as cursor:
            if isinstance(sql, str):
                cursor.execute(sql, params)
            else:
                for stmt in sql:
                    cursor.execute(stmt, params)
            if fetch:
                return cursor.fetchall()

    def session(self, **fields):
        return self.session_class(self, **fields)

    def trigger_name(self, model, trigger_type, prefix="tr"):
        table_name = split_identifier(model._meta.db_table)[1]
        return truncate_name(
            "{}_{}_{}".format(prefix, table_name, trigger_type.name.lower())
        )

    def create_trigger(self, model, trigger_type):
        raise NotImplementedError()

    def drop_trigger(self, model, trigger_type):
        raise NotImplementedError()
