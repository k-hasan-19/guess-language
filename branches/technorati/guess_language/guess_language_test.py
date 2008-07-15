# coding=utf-8

''' Copyright (c) 2008, Kent S Johnson 

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import unittest
import urllib

from guess_language import createOrderedModel, find_runs, guessLanguage, normalize, guessLanguageId, guessLanguageName,UNKNOWN

class guess_language_test(unittest.TestCase):
    def test_normalize(self):
        self.assertEquals('abc def ghi', normalize(u'abc4def   !@#!#@$   ghi'))
        
        s = u"På denne side bringer vi billeder fra de mange forskellige forberedelser til arrangementet efterhånden som vi får dem "
        self.assertEquals(s, normalize(s))
        
    def test_find_runs(self):
        self.assertEquals(['Basic Latin'], find_runs(u'This is a test of the language checker'))
        self.assertEquals(set(['Basic Latin', 'Extended Latin']), set(find_runs(u'abcdééé')))
        
        s = u"Сайлау нәтижесінде дауыстардың басым бөлігін ел премьер министрі Виктор Янукович пен оның қарсыласы, оппозиция жетекшісі Виктор Ющенко алды."
        self.assertEquals(['Cyrillic'], find_runs(s))
        
    
    def test_createOrderedModel(self):
        self.assertEquals([u'abc'], createOrderedModel(u'abc'))
        self.assertEquals(u'abc bca'.split(), createOrderedModel(u'abca'))
        self.assertEquals([u'cab', u'abc', u'abd', u'bca', u'bdc', u'dca'], createOrderedModel(u'abcabdcab'))
        
        
    def test_guess(self):
        tests = [
            ("This is a test of the language checker", "en"),
            ("Verifions que le détecteur de langues marche", "fr"),
            ("Sprawdźmy, czy odgadywacz języków pracuje", "pl"),
            ("авай проверить  узнает ли наш угадатель русски язык", "ru"),
            ("La respuesta de los acreedores a la oferta argentina para salir del default no ha sido muy positiv", "es"),
             ("Сайлау нәтижесінде дауыстардың басым бөлігін ел премьер министрі Виктор Янукович пен оның қарсыласы, оппозиция жетекшісі Виктор Ющенко алды.", "kk"), # Kazakh
            ("милиция ва уч солиқ идораси ходимлари яраланган. Шаҳарда хавфсизлик чоралари кучайтирилган.", "uz"), # uzbek
            ("көрбөгөндөй элдик толкундоо болуп, Кокон шаарынын көчөлөрүндө бир нече миң киши нааразылык билдирди.", "ky"), # kyrgyz
            ("yakın tarihin en çekişmeli başkanlık seçiminde oy verme işlemi sürerken, katılımda rekor bekleniyor.", "tr"), 
             ("Daxil olan xəbərlərdə deyilir ki, 6 nəfər Bağdadın mərkəzində yerləşən Təhsil Nazirliyinin binası yaxınlığında baş vermiş partlayış zamanı həlak olub.", "az"), # Azerbaijani

             (" ملايين الناخبين الأمريكيين يدلون بأصواتهم وسط إقبال قياسي على انتخابات هي الأشد تنافسا منذ عقود",  "ar"),
             ("Американське суспільство, поділене суперечностями, збирається взяти активну участь у голосуванні",  "uk"), # ukrainian
             ("Francouzský ministr financí zmírnil výhrady vůči nízkým firemním daním v nových členských státech EU",  "cs"), # czech
             ("biće prilično izjednačena, sugerišu najnovije ankete. Oba kandidata tvrde da su sposobni da dobiju rat protiv terorizma",  "hr"), # croatian
             (" е готов да даде гаранции, че няма да прави ядрено оръжие, ако му се разреши мирна атомна програма",  "bg"), # bulgarian
             ("на јавното мислење покажуваат дека трката е толку тесна, што се очекува двајцата соперници да ја прекршат традицијата и да се појават и на самиот изборен ден.",  "mk"), # macedonian
             ("în acest sens aparţinînd Adunării Generale a organizaţiei, în ciuda faptului că mai multe dintre solicitările organizaţiei privind organizarea scrutinului nu au fost soluţionate",  "ro"), # romanian
             ("kaluan ditën e fundit të fushatës në shtetet kryesore për të siguruar sa më shumë votues.",  "sq"), # albanian
             ("αναμένεται να σπάσουν παράδοση δεκαετιών και να συνεχίσουν την εκστρατεία τους ακόμη και τη μέρα των εκλογών",  "el"), # greek
             (" 美国各州选民今天开始正式投票。据信，",  "zh"), # chinese
             (" Die kritiek was volgens hem bitter hard nodig, omdat Nederland binnen een paar jaar in een soort Belfast zou dreigen te veranderen",  "nl"), # dutch
             ("På denne side bringer vi billeder fra de mange forskellige forberedelser til arrangementet, efterhånden som vi får dem ",  "da"), # danish
             ("Vi säger att Frälsningen är en gåva till alla, fritt och för intet.  Men som vi nämnt så finns det två villkor som måste",  "sv"), # swedish
             ("on julkishallinnon verkkopalveluiden yhteinen osoite. Kansalaisten arkielämää helpottavaa tietoa on koottu eri aihealueisiin",  "fi"), # finnish
             ("Ennetamaks reisil ebameeldivaid vahejuhtumeid vii end kurssi reisidokumentide ja viisade reeglitega ning muu praktilise informatsiooniga",  "et"), # estonian
             ("Hiába jön létre az önkéntes magyar haderő, hiába nem lesz többé bevonulás, változatlanul fennmarad a hadkötelezettség intézménye",  "hu"), # hungarian
             ("հարաբերական",  "hy"), # armenian
             ("Ikke bra. Jeg klarer vel 20 minutter med litt hjelp. Men jeg har ikke spilt fotball siden jeg la opp, så det er vanskelig å holde seg i form. Sykling hver dag er tungt og kjedelig, svarer Solskjær",  "no"), # norwegian
             ("ii",  UNKNOWN),
        ]

        for text, name in tests:
            self.assertEquals(name, guessLanguage(text))

    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
