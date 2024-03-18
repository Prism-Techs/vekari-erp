from rest_framework import serializers
from .models import DespatchMaster
from rest_framework.exceptions import ValidationError
from datetime import datetime


class MatchineDispatchSerializer(serializers.ModelSerializer):
    cmachineno = serializers.CharField(required=False)
    status = serializers.BooleanField(default=True, required=False)
    is_delete = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = DespatchMaster
        exclude = []
        extra_kwargs = {
            "cmachineno": {
                "required": False
            },
            "cmachno2": {
                "required": False
            },
            "status": {
                "required": False
            },
            "is_delete": {
                "required": False
            }
        }

    def create(self, validated_data):
        # user = self.context['request'].user
        cmachineno = validated_data.get('cmachineno')
        cmachno2 = validated_data.get('cmachno2')
        partNo = validated_data.get('cmodel')
        cyear = validated_data.get('cyear')

        date_object = datetime.now()
        year = str(date_object.year)
        # print(year)
        
        if year in cyear:
            partHas = DespatchMaster.objects.filter(cmodel=partNo).exists()
            # print(f"{year} is included in {cyear}")
            if partHas == True:
                cmachno2_data = DespatchMaster.objects.filter(cmodel=partNo).values('cmachno2').last()
                CMACHNO1 = validated_data.get('cmachno1',0)
                print(validated_data,CMACHNO1)

                if cmachno2 == None:
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2_data['cmachno2']+1)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2_data['cmachno2']+1
                else:
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2

            if partHas == False:
                CMACHNO1 = validated_data.get('cmachno1')

                # if cmachno2 == None:
                #     cmachno2 = 1
                #     cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                #     validated_data['cmachineno'] = cmachineno
                #     validated_data['cmachno2'] = cmachno2
                #     # print("cmachno2 is not has \n",validated_data)
                # else:
                cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                validated_data['cmachineno'] = cmachineno
                validated_data['cmachno2'] = cmachno2
        else:
            # print(f"{year} is not included in {cyear}")
            partHas = DespatchMaster.objects.filter(cmodel=partNo).exists()
            if partHas == True:
                cmachno2_data = DespatchMaster.objects.filter(cmodel=partNo).values('cmachno2').last()
                CMACHNO1 = validated_data.get('cmachno1')

                if cmachno2 == None:
                    cmachno2 = 1
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2
                else:
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2

            if partHas == False:
                CMACHNO1 = validated_data.get('cmachno1')

                if cmachno2 == None:
                    cmachno2 = 1
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2
                    # print("cmachno2 is not has \n",validated_data)
                else:
                    cmachno2 = 1
                    cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                    validated_data['cmachineno'] = cmachineno
                    validated_data['cmachno2'] = cmachno2
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
            print(instance.status)
            cmachineno = validated_data.get('cmachineno')
            cmachno2 = validated_data.get('cmachno2')
            partNo = validated_data.get('cmodel')
            cyear = validated_data.get('cyear')

            date_object = datetime.now()
            year = str(date_object.year)
            print(year)

            if instance.status:
                if year in cyear:
                    partHas = DespatchMaster.objects.filter(cmodel=partNo).exists()
                    print(f"{year} is included in {cyear}")
                    if partHas == True:
                        cmachno2_data = DespatchMaster.objects.filter(cmodel=partNo).values('cmachno2').last()
                        CMACHNO1 = validated_data.get('cmachno1')

                        if cmachno2 == None:
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2_data['cmachno2']+1)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2_data['cmachno2']+1
                        else:
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2

                    if partHas == False:
                        CMACHNO1 = validated_data.get('cmachno1')

                        # if cmachno2 == None:
                        #     cmachno2 = 1
                        #     cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                        #     validated_data['cmachineno'] = cmachineno
                        #     validated_data['cmachno2'] = cmachno2
                        #     # print("cmachno2 is not has \n",validated_data)
                        # else:
                        cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                        validated_data['cmachineno'] = cmachineno
                        validated_data['cmachno2'] = cmachno2
                else:

                    print(f"{year} is not included in {cyear}")
                    partHas = DespatchMaster.objects.filter(cmodel=partNo).exists()
                    if partHas == True:
                        cmachno2_data = DespatchMaster.objects.filter(cmodel=partNo).values('cmachno2').last()
                        CMACHNO1 = validated_data.get('cmachno1')

                        if cmachno2 == None:
                            cmachno2 = 1
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2
                        else:
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2

                    if partHas == False:
                        CMACHNO1 = validated_data.get('cmachno1')

                        if cmachno2 == None:
                            cmachno2 = 1
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2
                            # print("cmachno2 is not has \n",validated_data)
                        else:
                            cmachno2 = 1
                            cmachineno = "{}-{}".format(CMACHNO1, cmachno2)
                            validated_data['cmachineno'] = cmachineno
                            validated_data['cmachno2'] = cmachno2
            return super().update(instance, validated_data)
# {
#     "CNAM":"V. K. GOLD JEWELLERS",
#     "CCITY":"Jamnagar",
#     "CMACHNO1":"8910",
#     "CMACHNO2":"70004",
#     "NDESPACHNO":"32",
#     "DDESPATCDT":"2024-02-14",
#     "CEXTYPE":"Home",
#     "CMODEL":"MSH-820",
#     "CYEAR":"2024-25",
#     "CREMARK1":"test remark 1",
#     "CREMARK2":"test remark 2"
# }
