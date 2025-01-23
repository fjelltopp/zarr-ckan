import logging
from collections import OrderedDict
import ckanext.blob_storage.helpers as blobstorage_helpers
import ckan.lib.uploader as uploader
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.zarr.actions as zarr_actions
import ckanext.zarr.upload as zarr_upload
import ckanext.zarr.validators as zarr_validators
import ckanext.zarr.helpers as zarr_helpers
from ckan.lib.plugins import DefaultPermissionLabels
import ckan.model as model
from sqlalchemy import func


log = logging.getLogger(__name__)


class ZaRRPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IAuthenticator)

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'max_resource_size': uploader.get_max_resource_size,
            'get_dataset_from_id': zarr_helpers.get_dataset_from_id,
            'blob_storage_resource_filename': blobstorage_helpers.resource_filename,
            'get_facet_items_dict': zarr_helpers.get_facet_items_dict,
            'get_all_groups': zarr_helpers.get_all_groups,
            'get_user_from_id': zarr_helpers.get_user_from_id,
            'get_user_obj': zarr_helpers.get_user_obj,
            'month_formatter': zarr_helpers.month_formatter,
            'get_dataset_resource_type_groups': zarr_helpers.get_dataset_resource_type_groups
        }

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "zarr")

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
        new_fd = OrderedDict()
        new_fd['organization'] = plugins.toolkit._('Organizations')
        new_fd['tags'] = plugins.toolkit._('Tags')
        new_fd['groups'] = plugins.toolkit._('Topics')
        return new_fd

    # IResourceController
    def before_resource_create(self, context, resource):
        zarr_upload.handle_giftless_uploads(context, resource)
        return resource

    def before_resource_update(self, context, current, resource):
        zarr_upload.handle_giftless_uploads(context, resource, current=current)
        return resource

    # IActions
    def get_actions(self):
        return {
            'user_list': zarr_actions.user_list,
            'dataset_duplicate': zarr_actions.dataset_duplicate,
            'package_create': zarr_actions.package_create,
            'dataset_tag_replace': zarr_actions.dataset_tag_replace,
            'user_show_me': zarr_actions.user_show_me,
        }

    # IValidators
    def get_validators(self):
        return {
            'autogenerate_name_from_title': zarr_validators.autogenerate_name_from_title,
            'autofill': zarr_validators.autofill,
            'autogenerate': zarr_validators.autogenerate,
            'isomonth': zarr_validators.isomonth,
            'date_validator': zarr_validators.date_validator,
            'approval_required': zarr_validators.approval_required
        }

    # IPackageContoller
    def after_dataset_delete(self, context, data_dict):
        package_data = toolkit.get_action('package_show')(context, data_dict)
        if package_data.get('private'):
            package_data['state'] = 'deleted'
            context['package'].state = 'deleted'
            zarr_upload.add_activity(context, package_data, "changed")

    def after_dataset_update(self, context, data_dict):
        if data_dict.get('private'):
            zarr_upload.add_activity(context, data_dict, "changed")
        resource_type = data_dict.get('resource_type')
        if resource_type:
            zarr_actions.add_dataset_to_resource_type_group(resource_type, data_dict['id'])

    def after_dataset_create(self, context, data_dict):
        if data_dict.get('private'):
            zarr_upload.add_activity(context, data_dict, "new")
        resource_type = data_dict.get('resource_type')
        if resource_type:
            zarr_actions.add_dataset_to_resource_type_group(resource_type, data_dict['id'])

    def authenticate(self, identity):
        """
        verify is email is used | different case
        """
        if not identity or not identity.get('login') or not identity.get('password'):
            return None
        login = identity.get('login')
        password = identity.get('password')
        query = model.Session.query(model.User).filter(
            func.lower(model.User.email) == func.lower(login)
        )
        user = query.first()
        if user and user.is_active:
            if user.validate_password(password):
                return user
        return None

    def identify(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

