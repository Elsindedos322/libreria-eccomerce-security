from django.core.management.base import BaseCommand
from core.models import Categoria, Editorial, Autor, Libro
from datetime import date

# Helper to split full name into nombre and apellido
def split_name(full_name: str):
    parts = full_name.strip().split()
    if len(parts) == 1:
        # Fallback: use the same value for apellido if only one token is provided
        return parts[0], parts[0]
    apellido = parts[-1]
    nombre = " ".join(parts[:-1])
    return nombre, apellido

class Command(BaseCommand):
    help = 'Create sample books for testing'

    def handle(self, *args, **options):
        # Crear categorías
        categoria_ficcion, _ = Categoria.objects.get_or_create(nombre='Ficción')
        categoria_no_ficcion, _ = Categoria.objects.get_or_create(nombre='No Ficción')
        categoria_tecnico, _ = Categoria.objects.get_or_create(nombre='Técnico')
        categoria_educativo, _ = Categoria.objects.get_or_create(nombre='Educativo')
        categoria_ciencia, _ = Categoria.objects.get_or_create(nombre='Ciencia')
        categoria_historia, _ = Categoria.objects.get_or_create(nombre='Historia')
        categoria_fantasia, _ = Categoria.objects.get_or_create(nombre='Fantasía')
        categoria_infantil, _ = Categoria.objects.get_or_create(nombre='Infantil')
        categoria_romance, _ = Categoria.objects.get_or_create(nombre='Romance')
        categoria_misterio, _ = Categoria.objects.get_or_create(nombre='Misterio')
        categoria_biografia, _ = Categoria.objects.get_or_create(nombre='Biografía')
        categoria_autoayuda, _ = Categoria.objects.get_or_create(nombre='Autoayuda')
        categoria_negocios, _ = Categoria.objects.get_or_create(nombre='Negocios')
        categoria_psicologia, _ = Categoria.objects.get_or_create(nombre='Psicología')
        categoria_poetica, _ = Categoria.objects.get_or_create(nombre='Poesía')
        categoria_religion, _ = Categoria.objects.get_or_create(nombre='Religión')
        categoria_arte, _ = Categoria.objects.get_or_create(nombre='Arte')
        categoria_cocina, _ = Categoria.objects.get_or_create(nombre='Cocina')
        categoria_comic, _ = Categoria.objects.get_or_create(nombre='Cómic y Manga')
        categoria_deporte, _ = Categoria.objects.get_or_create(nombre='Deporte')
        categoria_viajes, _ = Categoria.objects.get_or_create(nombre='Viajes')
        categoria_tecnologia, _ = Categoria.objects.get_or_create(nombre='Tecnología')
        categoria_filosofia, _ = Categoria.objects.get_or_create(nombre='Filosofía')
        categoria_politica, _ = Categoria.objects.get_or_create(nombre='Política')

        # Crear editoriales
        editorial_tech, _ = Editorial.objects.get_or_create(nombre='TechBooks')
        editorial_fiction, _ = Editorial.objects.get_or_create(nombre='Fiction House')
        editorial_edu, _ = Editorial.objects.get_or_create(nombre='Educational Press')

        # Editoriales internacionales y locales conocidas
        editorial_penguin_rh, _     = Editorial.objects.get_or_create(nombre='Penguin Random House')
        editorial_hachette, _       = Editorial.objects.get_or_create(nombre='Hachette Livre')
        editorial_harpercollins, _  = Editorial.objects.get_or_create(nombre='HarperCollins Publishers')
        editorial_macmillan, _      = Editorial.objects.get_or_create(nombre='Macmillan Publishers')
        editorial_simon_schuster, _ = Editorial.objects.get_or_create(nombre='Simon & Schuster')
        editorial_scholastic, _     = Editorial.objects.get_or_create(nombre='Scholastic Corporation')
        editorial_abrams, _         = Editorial.objects.get_or_create(nombre='Abrams Books')
        editorial_cambridge_uni, _  = Editorial.objects.get_or_create(nombre='Cambridge University Press')
        editorial_harvard_uni, _    = Editorial.objects.get_or_create(nombre='Harvard University Press')
        editorial_basic_books, _    = Editorial.objects.get_or_create(nombre='Basic Books')
        editorial_bloomsbury, _     = Editorial.objects.get_or_create(nombre='Bloomsbury Publishing')
        editorial_planeta_peru, _    = Editorial.objects.get_or_create(nombre='Editorial Planeta Perú')
        editorial_santillana_peru, _ = Editorial.objects.get_or_create(nombre='Grupo Santillana Perú')
        editorial_horizonte, _       = Editorial.objects.get_or_create(nombre='Editorial Horizonte')
        editorial_fondo_pucp, _      = Editorial.objects.get_or_create(nombre='Fondo Editorial PUCP')
        editorial_bruño, _           = Editorial.objects.get_or_create(nombre='Asociación Editorial Bruño')
        editorial_cope, _            = Editorial.objects.get_or_create(nombre='Ediciones Copé')
        editorial_lexus_editores, _  = Editorial.objects.get_or_create(nombre='Lexus Editores')

        # Crear autores básicos de ejemplo
        autor_tech, _ = Autor.objects.get_or_create(nombre='Juan', apellido='Pérez')
        autor_fiction, _ = Autor.objects.get_or_create(nombre='María', apellido='García')
        autor_edu, _ = Autor.objects.get_or_create(nombre='Carlos', apellido='López')

        # Autores adicionales solicitados (se separa nombre y apellido automáticamente)
        n, a = split_name('William Shakespeare');            autor_shakespeare, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Jane Austen');                    autor_austen, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Charles Dickens');                autor_dickens, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('George Orwell');                  autor_orwell, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Ernest Hemingway');               autor_hemingway, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Leo Tolstoy');                    autor_tolstoy, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Fyodor Dostoevsky');              autor_dostoevsky, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Agatha Christie');                autor_christie, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Stephen King');                   autor_king, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('J.K. Rowling');                   autor_rowling, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('J.R.R. Tolkien');                 autor_tolkien, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Jules Verne');                    autor_verne, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Mark Twain');                     autor_twain, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Haruki Murakami');                autor_murakami, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Kazuo Ishiguro');                 autor_ishiguro, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Mario Vargas Llosa');             autor_vargas_llosa, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Julio Ramón Ribeyro');            autor_ribeyro, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('José María Arguedas');            autor_arguedas, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('César Vallejo');                  autor_vallejo, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Ricardo Palma');                  autor_palma, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Gabriela Wiener');                autor_wiener, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Renato Cisneros');                autor_cisneros, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Clorinda Matto de Turner');       autor_escuinte, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Juan de Espinosa Medrano');       autor_espinosa_medrano, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('José Carlos Mariátegui');         autor_mariategui, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Alfredo Bryce Echenique');        autor_bryce, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Jaime Bayly');                    autor_bayly, _ = Autor.objects.get_or_create(nombre=n, apellido=a)
        n, a = split_name('Claudia Ulloa Donoso');           autor_ulluadonoso, _ = Autor.objects.get_or_create(nombre=n, apellido=a)

        # Crear libros
        libros_data = [
            {
                'titulo': 'Introducción a Django',
                'descripcion': 'Un libro completo sobre desarrollo web con Django',
                'precio': 29.99,
                'stock': 10,
                'categoria': categoria_tecnico,
                'editorial': editorial_tech,
                'fecha_publicacion': date(2024, 1, 1),
                'autores': [autor_tech]
            },
            {
                'titulo': 'Python para Principiantes',
                'descripcion': 'Aprende Python desde cero',
                'precio': 24.99,
                'stock': 15,
                'categoria': categoria_educativo,
                'editorial': editorial_edu,
                'fecha_publicacion': date(2023, 6, 15),
                'autores': [autor_edu]
            },
            {
                'titulo': 'El Misterio del Código',
                'descripcion': 'Una novela de suspense tecnológico',
                'precio': 19.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(2024, 3, 10),
                'autores': [autor_fiction]
            },
            {
                'titulo': 'API REST con Django',
                'descripcion': 'Desarrollo de APIs REST seguras',
                'precio': 34.99,
                'stock': 12,
                'categoria': categoria_tecnico,
                'editorial': editorial_tech,
                'fecha_publicacion': date(2024, 2, 20),
                'autores': [autor_tech]
            },
            {
                'titulo': 'Seguridad en Aplicaciones Web',
                'descripcion': 'Guía completa de seguridad web',
                'precio': 39.99,
                'stock': 5,
                'categoria': categoria_tecnico,
                'editorial': editorial_tech,
                'fecha_publicacion': date(2024, 4, 5),
                'autores': [autor_tech, autor_edu]
            },
            # Shakespeare
            {
                'titulo': 'Hamlet',
                'descripcion': 'Tragedia clásica de intriga y venganza',
                'precio': 14.99,
                'stock': 12,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1603, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Macbeth',
                'descripcion': 'Tragedia sobre la ambición desmedida',
                'precio': 13.99,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1606, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Romeo and Juliet',
                'descripcion': 'Romance clásico lleno de pasión y conflicto familiar',
                'precio': 12.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1597, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'A Midsummer Night’s Dream',
                'descripcion': 'Comedia mágica de William Shakespeare en un bosque encantado',
                'precio': 15.99,
                'stock': 11,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1595, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Merchant of Venice',
                'descripcion': 'Obra de Shakespeare sobre justicia, deuda y venganza',
                'precio': 14.50,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1596, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'As You Like It',
                'descripcion': 'Comedia romántica de Shakespeare',
                'precio': 13.75,
                'stock': 12,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1599, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Julius Caesar',
                'descripcion': 'Tragedia de Shakespeare sobre poder y traición',
                'precio': 14.25,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1599, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Twelfth Night',
                'descripcion': 'Comedia de enredos y disfraz de Shakespeare',
                'precio': 13.99,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1605, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'King Lear',
                'descripcion': 'Tragedia de Shakespeare sobre vejez, poder y traición',
                'precio': 15.50,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1606, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Othello',
                'descripcion': 'Tragedia de Shakespeare sobre celos y manipulación',
                'precio': 14.95,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1604, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Winter’s Tale',
                'descripcion': 'Tragedia/Comedia tardía de Shakespeare sobre redención y tiempo',
                'precio': 15.00,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1611, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'All’s Well That Ends Well',
                'descripcion': 'Una de las últimas comedias de Shakespeare, sobre amor y clases sociales',
                'precio': 14.20,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1604, 1, 1),
                'autores': [autor_shakespeare]
            },
            # Mario Vargas Llosa
            {
                'titulo': 'The Time of the Hero',
                'descripcion': 'Novela de Mario Vargas Llosa sobre la vida en una academia militar en Lima',
                'precio': 18.99,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1963, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Feast of the Goat',
                'descripcion': 'Novela histórica de Vargas Llosa ambientada en la República Dominicana',
                'precio': 19.99,
                'stock': 6,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(2000, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Green House',
                'descripcion': 'Obra de Vargas Llosa situada entre la selva y el desierto peruanos',
                'precio': 17.99,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1966, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Bad Girl',
                'descripcion': 'Novela de Vargas Llosa sobre obsesión y expatriados',
                'precio': 16.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(2006, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Death in the Andes',
                'descripcion': 'Novela de Vargas Llosa ambientada en la sierra peruana y el conflicto armado',
                'precio': 18.50,
                'stock': 5,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1993, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'In Praise of the Stepmother',
                'descripcion': 'Novela de Vargas Llosa sobre deseo y moralidad',
                'precio': 17.25,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1988, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Conversation in the Cathedral',
                'descripcion': 'Novela de Vargas Llosa sobre corrupción política en el Perú de los años 50',
                'precio': 19.75,
                'stock': 6,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1969, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Storyteller',
                'descripcion': 'Novela de Vargas Llosa sobre la cultura indígena y narrativa en Perú',
                'precio': 16.50,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1987, 1, 1),
                'autores': [autor_vargas_llosa]
            },
        ]

        for libro_data in libros_data:
            autores = libro_data.pop('autores')
            libro, created = Libro.objects.get_or_create(
                titulo=libro_data['titulo'],
                defaults=libro_data
            )
            if created:
                libro.autores.set(autores)
                self.stdout.write(self.style.SUCCESS(f'Created book: {libro.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {libro.titulo}'))

        # Libros adicionales
        libros_data_extra = [
            {
                'titulo': 'The Feast of the Goat',
                'descripcion': 'Novela histórica de corrupción y dictadura en República Dominicana',
                'precio': 19.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(2000, 6, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The War of the End of the World',
                'descripcion': 'Gran novela de conflicto social en Brasil, del autor peruano',
                'precio': 18.99,
                'stock': 6,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1981, 10, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Dream of the Celt',
                'descripcion': 'Novela biográfica sobre Roger Casement por Vargas Llosa',
                'precio': 17.50,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(2010, 11, 3),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Letters to a Young Novelist',
                'descripcion': 'Ensayo guía sobre la escritura, del autor peruano',
                'precio': 16.99,
                'stock': 10,
                'categoria': categoria_educativo,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1997, 5, 15),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Harry Potter and the Philosopher’s Stone',
                'descripcion': 'El primer libro de la saga de magos más famosa',
                'precio': 24.99,
                'stock': 20,
                'categoria': categoria_ficcion,
                'editorial': editorial_penguin_rh,
                'fecha_publicacion': date(1997, 6, 26),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'Harry Potter and the Chamber of Secrets',
                'descripcion': 'Segunda entrega de la saga de Harry Potter',
                'precio': 24.99,
                'stock': 18,
                'categoria': categoria_ficcion,
                'editorial': editorial_penguin_rh,
                'fecha_publicacion': date(1998, 7, 2),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'Harry Potter and the Prisoner of Azkaban',
                'descripcion': 'Tercera entrega de la saga de Harry Potter',
                'precio': 24.99,
                'stock': 15,
                'categoria': categoria_ficcion,
                'editorial': editorial_penguin_rh,
                'fecha_publicacion': date(1999, 7, 8),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'Fantastic Beasts and Where to Find Them',
                'descripcion': 'Libro complementario al universo de Harry Potter',
                'precio': 19.99,
                'stock': 12,
                'categoria': categoria_comic if 'categoria_comic' in locals() else categoria_ficcion,
                'editorial': editorial_scholastic,
                'fecha_publicacion': date(2001, 3, 1),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'The Christmas Pig',
                'descripcion': 'Libro infantil/familiar de la autora de Harry Potter',
                'precio': 18.99,
                'stock': 14,
                'categoria': categoria_infantil,
                'editorial': editorial_scholastic,
                'fecha_publicacion': date(2021, 10, 12),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'Macbeth',
                'descripcion': 'Tragedia de poder y ambición de Shakespeare',
                'precio': 15.99,
                'stock': 13,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1606, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'King Lear',
                'descripcion': 'Obra maestra tardía de Shakespeare sobre el poder y la vejez',
                'precio': 15.50,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1606, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Othello',
                'descripcion': 'Tragedia de los celos y manipulación de Shakespeare',
                'precio': 14.95,
                'stock': 11,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1604, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'Twelfth Night',
                'descripcion': 'Comedia de enredos de Shakespeare',
                'precio': 13.99,
                'stock': 12,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1605, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'As You Like It',
                'descripcion': 'Comedia romántica de Shakespeare sobre disfraz y bosque',
                'precio': 13.75,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1599, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Green House',
                'descripcion': 'Novela de Vargas Llosa situada entre el desierto y la selva',
                'precio': 17.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1966, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'A Midsummer Night’s Dream',
                'descripcion': 'Comedia mágica de Shakespeare en un bosque encantado',
                'precio': 15.99,
                'stock': 11,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1595, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Time of the Hero',
                'descripcion': 'Novela de Vargas Llosa sobre la vida en una academia militar en Lima',
                'precio': 18.99,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1963, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'All’s Well That Ends Well',
                'descripcion': 'Comedia tardía de Shakespeare sobre clases sociales y redención',
                'precio': 14.20,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1604, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Bad Girl',
                'descripcion': 'Novela de Vargas Llosa sobre obsesión y expatriados',
                'precio': 16.99,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(2006, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'The Storyteller',
                'descripcion': 'Novela de Vargas Llosa sobre la cultura indígena en Perú',
                'precio': 16.50,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1987, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Death in the Andes',
                'descripcion': 'Novela de Vargas Llosa ambientada en la sierra peruana y Sendero Luminoso',
                'precio': 18.50,
                'stock': 5,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1993, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Hamlet',
                'descripcion': 'Una de las tragedias más profundas de Shakespeare',
                'precio': 15.99,
                'stock': 10,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1603, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Cubs and Other Stories',
                'descripcion': 'Colección de cuentos de Vargas Llosa sobre juventud machista en Perú',
                'precio': 14.99,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1979, 8, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Aunt Julia and the Scriptwriter',
                'descripcion': 'Novela semi-autobiográfica de Vargas Llosa ambientada en Lima',
                'precio': 17.25,
                'stock': 7,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1977, 7, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Pantaleón and the Special Services',
                'descripcion': 'Sátira del servicio militar en la Amazonía peruana por Vargas Llosa',
                'precio': 16.75,
                'stock': 8,
                'categoria': categoria_ficcion,
                'editorial': editorial_planeta_peru,
                'fecha_publicacion': date(1973, 1, 1),
                'autores': [autor_vargas_llosa]
            },
            {
                'titulo': 'Twelfth Night (Spanish edition)',
                'descripcion': 'Versión en español de la comedia de Shakespeare',
                'precio': 13.50,
                'stock': 11,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1602, 1, 1),
                'autores': [autor_shakespeare]
            },
            {
                'titulo': 'The Ickabog',
                'descripcion': 'Cuento infantil y fantástico de J.K. Rowling',
                'precio': 18.50,
                'stock': 14,
                'categoria': categoria_infantil,
                'editorial': editorial_scholastic,
                'fecha_publicacion': date(2020, 11, 10),
                'autores': [autor_rowling]
            },
            {
                'titulo': 'The Merchant of Venice',
                'descripcion': 'Obra de teatro de Shakespeare sobre justicia, deuda y amistad',
                'precio': 14.25,
                'stock': 9,
                'categoria': categoria_ficcion,
                'editorial': editorial_fiction,
                'fecha_publicacion': date(1596, 1, 1),
                'autores': [autor_shakespeare]
            },
        ]

        for libro_data in libros_data_extra:
            autores = libro_data.pop('autores')
            libro, created = Libro.objects.get_or_create(
                titulo=libro_data['titulo'],
                defaults=libro_data
            )
            if created:
                libro.autores.set(autores)
                self.stdout.write(self.style.SUCCESS(f'Libro creado: {libro.titulo}'))
            else:
                self.stdout.write(self.style.WARNING(f'Este libro ya existe oeee: {libro.titulo}'))

        self.stdout.write(self.style.SUCCESS('Creacion de libros completada!'))