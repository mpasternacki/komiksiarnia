from django.db import connection
from django.contrib.auth.models import User
import phpserialize
from tagging.models import Tag
from komiksy.models import Seria, Pasek
from lusers.models import UserProfile

cursor = connection.cursor()

def migrate_users():
    cursor.execute("SELECT * FROM users;")
    idmap = {}
    for id, username, password, strips, last_visit, max_id, site_message in cursor.fetchall():
        print 'migrate %s' % username

        u = User.objects.create_user(username, '', password)
        u.last_login = last_visit
        u.save()

        p = UserProfile(user=u, max_id=max_id)
        p.save()
        p.serie_ignorowane = Seria.objects.filter(
            tytul__in=phpserialize.dict_to_tuple(phpserialize.loads(strips)))
        p.save()

        idmap[id] = u.id

def migrate_paski():
    cursor.execute("ALTER TABLE paski DROP COLUMN keywords;")
    cursor.execute("ALTER TABLE paski ADD COLUMN tagi VARCHAR(255) NOT NULL;");

def _migrate_old_tags():
    for fr, to in idmap.items():
        cursor.execute("UPDATE tagi SET autor=%s WHERE autor=%s;", (fr, -to))
    cursor.execute("UPDATE tagi SET autor=-autor;")
    cursor.execute("ALTER TABLE tagi ADD COLUMN id INT NOT NULL PRIMARY KEY AUTO_INCREMENT;")

def migrate_tags():
    # clean up
    cursor.execute('DELETE FROM tagi USING tagi,paski WHERE tagi.pasek=paski.id AND tagi.tag=SUBSTRING(paski.tytul_paska FROM 1 FOR LENGTH(tagi.tag));');
    cursor.execute('DELETE FROM tagi WHERE NOT EXISTS (SELECT * FROM paski WHERE paski.id=tagi.pasek);')
    cursor.execute("DELETE FROM tagi WHERE tag LIKE '#%';")

    cursor.execute("SELECT * FROM tagi;")
    for pasek_id, tag_name, user_id, seria_id, tag_id in cursor.fetchall():
        pasek = Pasek.objects.get(id=pasek_id)
        if not tag_name: continue
        try: tag_name = tag_name.encode('iso-8859-1').decode('iso-8859-2')
        except UnicodeEncodeError: pass
        Tag.objects.add_tag(pasek, '"%s"'%tag_name)

def migrate():
    migrate_users()
    migrate_paski()
    migrate_tags()

def drop_migrated():
    cursor.execute("DROP TABLE tagi;")
    cursor.execute("DROP TABLE tag;")
    cursor.execute("DROP TABLE tag_pasek;")
    cursor.execute("DROP TABLE users;")
    cursor.execute("DROP TABLE subscriptions;")
