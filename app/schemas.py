from app import ma


# class CourseSchema(ma.Schema):
#     class Meta:
#         fields = ('name',)
#
#
# class GroupSchema(ma.Schema):
#     class Meta:
#         fields = ('name',)


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'group', 'courses')
