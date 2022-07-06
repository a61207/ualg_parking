# Generated by Django 4.0.4 on 2022-07-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='park',
            name='city',
            field=models.CharField(choices=[('11', 'Lisbon'), ('12', 'Lisbon'), ('13', 'Lisbon'), ('14', 'Lisbon'), ('15', 'Lisbon'), ('16', 'Lisbon'), ('18', 'Lisbon'), ('19', 'Lisbon'), ('20', 'Santarém'), ('21', 'Coruche'), ('22', 'Abrantes'), ('23', 'Tomar'), ('24', 'Leiria'), ('25', 'Caldas da Rainha'), ('26', 'Vila Franca de Xira'), ('27', 'Amadora'), ('28', 'Almada'), ('29', 'Setúbal'), ('30', 'Coimbra'), ('31', 'Pombal'), ('32', 'Lousã'), ('33', 'Arganil'), ('35', 'Oliveira do Hospital'), ('34', 'Viseu'), ('36', 'Castro Daire'), ('37', 'São João da Madeira'), ('38', 'Aveiro'), ('40', 'Porto'), ('41', 'Porto'), ('42', 'Porto'), ('43', 'Porto'), ('44', 'Vila Nova de Gaia'), ('45', 'Espinho'), ('46', 'Amarante'), ('47', 'Braga'), ('48', 'Guimarães'), ('49', 'Viana do Castelo'), ('50', 'Vila Real'), ('51', 'Lamego'), ('52', 'Mogadouro'), ('53', 'Bragança'), ('54', 'Chaves'), ('60', 'Castelo Branco'), ('61', 'Sertã'), ('62', 'Covilhã'), ('63', 'Guarda'), ('64', 'Pinhel'), ('70', 'Évora'), ('71', 'Estremoz'), ('72', 'Reguengos de Monsaraz'), ('73', 'Portalegre'), ('74', 'Ponte de Sôr'), ('75', 'Vila Nova de Santo André'), ('76', 'Aljustrel'), ('77', 'Almodôvar'), ('78', 'Beja'), ('80', 'Faro'), ('81', 'Loulé'), ('82', 'Albufeira'), ('83', 'Silves'), ('84', 'Lagoa'), ('85', 'Portimão'), ('86', 'Lagos'), ('87', 'Olhão'), ('88', 'Tavira'), ('89', 'Vila Real de Santo António'), ('90', 'Funchal'), ('91', 'Santa Cruz'), ('92', 'Machico'), ('93', 'Câmara de Lobos'), ('94', 'Porto Santo'), ('95', 'Ponta Delgada'), ('96', 'Ribeira Grange'), ('97', 'Angra do Heroísmo'), ('98', 'Velas'), ('99', 'Horta')], db_column='City', max_length=2, null=True, verbose_name='City'),
        ),
    ]
