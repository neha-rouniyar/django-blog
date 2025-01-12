from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    formatted_date=serializers.SerializerMethodField()

    class Meta:
        model=Blog
        # fields=[
        #      "id",
        #     "title",
        #     "author_name",
        #     "category",
        #     "description",
        #     "formatted_date"
        #     ]
         # for getting all fields including id
        fields = "__all__"
    def get_formatted_date(self,obj):
            return obj.published_date.strftime("%d/%m/%y")

       

        ## for excluding certain column values while in a large table columns
        # exclude=['author_name','category']


class BlogFieldsSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    author_name=serializers.EmailField()


    ## to check if the title contains a word 'badword'
    # def validate_title(self, value):
    #     if "badword" in value:
    #         raise serializers.ValidationError("Title contains prohibited words.")
    #     return value