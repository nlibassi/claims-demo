try:
        patient = Insured.query. \
            filter(Insured.first_name==patient_name_first and \
                Insured.middle_name==patient_name_middle and \
                Insured.last_name==patient_name_last).first()
        claim = Claim(insured_id=current_user.id)
    except:
        patient = Dependent.query. \
            filter(Dependent.first_name==patient_name_first and \
                Dependent.middle_name==patient_name_middle and \
                Dependent.last_name==patient_name_last).first()
