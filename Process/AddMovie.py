from Modals.Register import register_modal
from Includes import Dbh
from Classes import MoviesCntrl_Class
from Modals.Message import message_modal

def addMovie(self):
    # Get data from modal (modal must return a dict)
    movie_data = register_modal(self)

    if not movie_data:
        return  # User canceled modal

    # Create controller
    controller = MoviesCntrl_Class(
        title=movie_data['title'],
        genre=movie_data['genre'],
        price=movie_data['price'],
        duration=movie_data['duration'],
        rating=movie_data['rating'],
        status=movie_data['status'],
        description=movie_data['description'],
        poster_path=movie_data['poster']
    )

    # Save movie
    ok, msg = controller.save()

    # Show message
    if ok:
        message_modal(self, msg if msg else "Movie added successfully!", success=True)
    else:
        message_modal(self, msg if msg else "Failed to add movie.", success=False)
