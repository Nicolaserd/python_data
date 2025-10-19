
import os, csv, unicodedata, re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.conf import settings
from dashboards.models import Dashboard
from dotenv import load_dotenv

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

class Command(BaseCommand):
    help = "Crea usuarios/grupo desde .env e importa dashboards desde CSV (con contraseñas encriptadas)."

    def handle(self, *args, **kwargs):
        load_dotenv(settings.BASE_DIR / '.env')

        # Grupo de privados
        group_name = os.getenv('PRIVATE_GROUP_NAME', 'Privados')
        group, _ = Group.objects.get_or_create(name=group_name)
        self.stdout.write(self.style.SUCCESS(f"Grupo listo: {group_name}"))

        # Crear/actualizar usuarios con set_password (encripta)
        users_data = [
            ('ADMIN_', True),
            ('USER_PRIVADO_', False),
            ('USER_PUBLICO_', False),
        ]
        for prefix, is_super in users_data:
            u = os.getenv(prefix+'USERNAME')
            p = os.getenv(prefix+'PASSWORD')
            e = os.getenv(prefix+'EMAIL')
            if not u or not p:
                continue
            user, created = User.objects.get_or_create(username=u, defaults={'email': e or ''})
            user.email = e or ''
            user.is_superuser = is_super
            user.is_staff = True if is_super else False
            user.set_password(p)  # ENCRIPTA
            user.save()
            if prefix == 'USER_PRIVADO_':
                user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f"Usuario listo: {u} (superuser={is_super})"))

        # Importar CSV
        csv_path = settings.BASE_DIR / os.getenv('CSV_PATH', 'data/dashboards.csv')
        nb_base = settings.BASE_DIR / os.getenv('NOTEBOOKS_PATH', 'notebooks')
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"No se encontró CSV en {csv_path}"))
            return

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                area = row.get('area','').strip()
                nombre = row.get('nombre','').strip()
                fuente = row.get('fuente','').strip()
                link = row.get('linkapowerbi','').strip()
                esprivado = str(row.get('esprivado','')).strip().lower() in ('true','1','sí','si')
                # notebook path heuristic
                # Search by original name first, then slug
                candidates = [
                    nb_base / area / f"{nombre}.ipynb",
                    nb_base / area / f"{slugify(nombre)}.ipynb",
                ]
                nb_path = None
                for c in candidates:
                    if c.exists():
                        nb_path = c.relative_to(settings.BASE_DIR).as_posix()
                        break

                d, created = Dashboard.objects.get_or_create(
                    area=area, nombre=nombre,
                    defaults={'fuente':fuente,'linkapowerbi':link,'esprivado':esprivado,'notebook_path':nb_path}
                )
                if not created:
                    d.fuente, d.linkapowerbi, d.esprivado, d.notebook_path = fuente, link, esprivado, nb_path
                    d.save()
                count += 1
            self.stdout.write(self.style.SUCCESS(f"Importados/actualizados {count} dashboards"))
