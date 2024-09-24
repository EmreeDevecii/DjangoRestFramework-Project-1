from rest_framework import serializers
from haberler.models import Makale, Gazeteci

from datetime import datetime
from datetime import date
from django.utils.timesince import timesince




class MakaleSerializer(serializers.ModelSerializer):

    time_since_pub = serializers.SerializerMethodField()
    # yazar = serializers.StringRelatedField()
    # yazar = GazeteciSerializer()

    class Meta:
        model = Makale
        fields = '__all__'
        # fields = ['yazar', 'baslik', 'metin']
        # exclude = ['yazar', 'baslik', 'metin']
        read_only_fields = ['id', 'yayimlanma_tarihi', 'güncellenme_tarihi']

    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayimlanma_tarihi
        if object.aktif is True:
            time_delta = timesince(pub_date, now)
            return time_delta
        else:
            return 'Aktif Değil'
    
    def validate_yayimlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yaymlanma tarihi ileri bir tarih olamaz!')
        return tarihdegeri


class GazeteciSerializer(serializers.ModelSerializer):

    # makaleler = MakaleSerializer(many=True, read_only=True)
    makaleler = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name = 'makale-detay',
    )


    class Meta:
        model = Gazeteci
        fields = '__all__'









#Standart Serializer#
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayimlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncellenme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance
    
    def validate(self, data): # object level
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Baslik ve açıklama alanları aynı olamaz. Lütfen farklı bir açıklama giriniz')
        return data
    
    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Baslik alani minimum 20 karakter olmalı. siz {len(value)} karakter girdiniz')
        return value

