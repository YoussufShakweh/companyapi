from drf_yasg.inspectors import SwaggerAutoSchema


class CompoundTagsSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        return ["_".join(operation_keys[:-1])]
