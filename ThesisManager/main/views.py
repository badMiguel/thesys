from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')







class Thesis:
    def __init__(self, topic_number, casuarina, sydney, external, 
                 chem_engineering, civ_engineering, elec_engineering, mech_engineering, comp_sci, cyber_sec, data_sci, info_syst, software_engineer,
                 category,  title, thesis_supervisor, description):
        self.topic_number = topic_number
        self.casuarina = casuarina
        self.sydney = sydney
        self.external = external
        self.chem_engineering = chem_engineering
        self.civ_engineering = civ_engineering
        self.elec_engineering = elec_engineering
        self.mech_engineering = mech_engineering
        self.comp_sci = comp_sci
        self.cyber_sec = cyber_sec
        self.data_sci = data_sci
        self.info_syst = info_syst
        self.software_engineer = software_engineer
        self.category = category
        self.title = title
        self.thesis_supervisor = thesis_supervisor
        self.description = description