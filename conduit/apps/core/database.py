from django.core.exceptions import ObjectDoesNotExist
from django.db import (DatabaseError, IntegrityError, OperationalError,
                       transaction)
from graphql import GraphQLError

from conduit.apps.core.exceptions import errors


class SaveContextManager():
    """
    Manage database exceptions during saving and updating actions.

    Args:
        model_instance(class instance): Holds the instance to be saved/updated.
        kwargs : Hold optional keyword arguments.

    Attributes:
        model: Holds the model for the instance we are saving/updating.

    Returns:
        model_instance: If the action(save/update) is successful.
        error: Else exception is raised with appropriate message.
    """

    def __init__(self, model_instance):
        self.model_instance = model_instance

    def __enter__(self):
        try:
            with transaction.atomic():
                self.model_instance.save()
            return self.model_instance
        except (IntegrityError, DatabaseError, OperationalError) as e:
            raise GraphQLError(str(e))

    def __exit__(self, exception_type, exception_value, traceback):
        return False


def get_model_object(model, column_name, column_value, **kwargs):
    """
    Gets model instance from the database by a certain field.

    Args:
        model: Holds the model from which we want to query data
        column_name: Holds the model field to query data by from the model.
        column_value: Holds the value for the column_name.
        kwargs : Hold optional keyword arguments.
        message: Holds a custom error message(it's optional).
        error: Holds a error type to raise in case it's not GraphQlError
               (it's optional).

    Returns:
        model_instance: If the value exists or not, at checks of
         column_name id having column_value as an int and
         greater or equal to one, or column_name id having
         column_value as a string, or any other column_name being
         any name other than id.
        error: Else exception is raised with appropriate message.
    """
    try:
        model_instance = model.objects.get(**{column_name: column_value})
        return model_instance
    except ObjectDoesNotExist:
        message = kwargs.get('message', None)
        error_type = kwargs.get('error_type', None)
        if message is not None:
            errors.custom_message(message, error_type=error_type)
        errors.db_object_do_not_exists(
            model.__name__, column_name, column_value, error_type=error_type)