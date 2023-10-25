from FoodyCore.extension import db
from FoodyAuth.model import Section


def get_all_unique_sections_wtf_select():
    """
        this function return all sections in a wtf.selectForm

        like:
        [
            (SectionPublicKey, SectionName),
            ...
        ]

    """
    sections = [(each[0], each[0]) for each in db.session.query(Section.Name).distinct().all()]
    extra = [("all", "همه بخش ها")]
    data = []

    for each in sections:
        s = Section.query.filter_by(Name=each[0]).first()
        data.append((s.PublicKey, s.Name))

    data = data + extra
    return data
