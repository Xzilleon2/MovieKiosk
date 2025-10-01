from Modals.Register import register_modal

def addMovie(self, movie_data):
    if not movie_data:
        print("User canceled or closed modal.")
        return

    print("Movie data received in addMovie:")
    for key, value in movie_data.items():
        print(f"  {key}: {value}")
