from rest_framework import serializers

from igmain.models import IGaccount, IGmodel, IGpublic


class IGaccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = IGaccount
        fields = ("igaccount",)


class IGmodelSerializers(serializers.ModelSerializer):
    class Meta:
        model = IGmodel
        fields = ("igmodel", 'msg_status')

class IGpublicSerializers(serializers.ModelSerializer):
    class Meta:
        model = IGpublic
        fields = ("igpublic",)
