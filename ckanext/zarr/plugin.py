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

log = logging.getLogger(__name__)


class WHOAFROPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'max_resource_size': uploader.get_max_resource_size,
            'get_dataset_from_id': zarr_helpers.get_dataset_from_id,
            'blob_storage_resource_filename': blobstorage_helpers.resource_filename,
            'get_facet_items_dict': zarr_helpers.get_facet_items_dict,
            'get_all_groups': zarr_helpers.get_all_groups,
            'get_featured_datasets': zarr_helpers.get_featured_datasets,
            'get_user_from_id': zarr_helpers.get_user_from_id,
            'get_user_obj': zarr_helpers.get_user_obj,
            'month_formatter': zarr_helpers.month_formatter,
        }

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "zarr")

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
        new_fd = OrderedDict()
        new_fd['program_area'] = plugins.toolkit._('Program Areas')
        new_fd['tags'] = plugins.toolkit._('Tags')
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
            'isomonth': zarr_validators.isomonth
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

    def after_dataset_create(self, context, data_dict):
        if data_dict.get('private'):
            zarr_upload.add_activity(context, data_dict, "new")
