# Auctions

An eBay-style auction site built with **Django**. Users can create listings, bid on items, comment, keep a watchlist, and browse by category. Data is stored in a relational database through Django's ORM, and pages are styled with **Bootstrap 4**.

This is my implementation of **Project 2: Commerce** from [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/).

---

## Features

| Feature | Behavior |
| --- | --- |
| **Active listings** | The home page shows every listing that has not been sold, with its image, title, description, and current bid. Each title links to the listing page. |
| **Register / Log in / Log out** | Users create an account with a username, email, and password (confirmed twice). Duplicate usernames and mismatched passwords show an error message. |
| **Create listing** | Signed-in users open "Create Listing" and enter a title, description, and starting price. An image URL and a category are optional. |
| **Listing page** | Shows the image, description, current bid, category, seller, and posting date. Signed-in users get the bid, watchlist, and comment controls. |
| **Bidding** | A bid must be at least the starting price and higher than any earlier bid. If it is invalid, an error message explains why and nothing is saved. |
| **Watchlist** | Signed-in users add a listing to their watchlist from the listing page, and remove it from the Watchlist page. |
| **Close auction** | Only the seller sees a "Close" button. Closing marks the listing as sold and makes the highest bidder the winner. |
| **Bought items** | The "Bought Items" page lists every auction the user has won. A winner also sees a "you won!" message on the listing page. |
| **Comments** | Signed-in users can comment on any listing. Comments show the author, text, and time. |
| **Categories** | The Categories page lists every category that has an active listing. Each category links to the listings in it. |

---

## Getting Started

**Requirements:** Python 3.8+

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd commerce

# 2. Install dependencies
pip install django

# 3. Create and apply the database migrations
python manage.py makemigrations auctions
python manage.py migrate

# 4. Run the development server
python manage.py runserver
```

Then open <http://127.0.0.1:8000/> in your browser and register an account.

To use the Django admin, create a superuser with `python manage.py createsuperuser` and visit `/admin`.

---
## Demo Video
[![Watch the demo](https://img.youtube.com/vi/XB9h76ytXIE/maxresdefault.jpg)](https://youtu.be/XB9h76ytXIE)

## Project Structure

```text
commerce/
├── manage.py
├── commerce/                      # Project configuration
│   ├── settings.py                # Sets AUTH_USER_MODEL = "auctions.User"
│   └── urls.py                    # Includes the auctions app's URLs
│
└── auctions/                      # Main app
    ├── models.py                  # User, Listing, Comments
    ├── views.py                   # All page and form handlers
    ├── urls.py                    # App routes
    ├── static/auctions/
    │   └── styles.css             # Extra styling on top of Bootstrap
    └── templates/auctions/
        ├── layout.html            # Base template: navbar, sign-in status
        ├── index.html             # Active listings
        ├── listing.html           # Listing details, bidding, comments
        ├── createlist.html        # New listing form
        ├── watchlist.html         # User's watchlist
        ├── bought.html            # Items the user has won
        ├── categories.html        # List of categories
        ├── listbycategory.html    # Listings in one category
        ├── login.html             # Log in form
        └── register.html          # Registration form
```

---

## Data Models

| Model | Fields |
| --- | --- |
| `User` | Extends Django's `AbstractUser`. Adds a `watchlist` many-to-many relation to `Listing`. |
| `Listing` | `title`, `description`, `image` (URL), `category`, `bidding` (current bid), `original` (starting price), `bidcount`, `date`, `sold`, plus relations to `listed_by` (seller), `currentbidder` (highest bidder), and `owner` (winner). |
| `Comments` | `text`, `datetime`, plus relations to the `commentor` (author) and the `listing` it belongs to. |

---

## How It Works

Each route in `auctions/urls.py` maps to one view in `auctions/views.py`:

| Route | View | Description |
| --- | --- | --- |
| `/` | `index` | Renders all listings; the template shows only those that are not sold. |
| `/login`, `/logout`, `/register` | `login_view`, `logout_view`, `register` | Authentication. Registration logs the new user in automatically. |
| `/createlist` | `create_listing` | On `GET`, shows the form. On `POST`, saves the listing with the seller set to the current user and redirects to the home page. |
| `/listing/<id>` | `listing` | Renders one listing with its comments. |
| `/bid` | `bid` | Checks the bid against the starting price and the current bid. If it is valid, it updates the listing's current bid, bid count, and highest bidder. |
| `/close` | `closelisting` | Marks the listing as sold and adds it to the highest bidder's owned items. |
| `/watchlist`, `/watchlist/add`, `/watchlist/remove` | `watchlist`, `add`, `remove` | Shows, adds to, and removes from the user's watchlist. |
| `/bought` | `boughtitems` | Lists the auctions the user has won. |
| `/comment` | `comment` | Saves a comment on a listing and redirects back to it. |
| `/categories` | `categories` | Lists distinct categories that have active listings. |
| `/categoricallist/<category>` | `categoricallist` | Lists the listings in one category. |

Views that change data or show personal pages use Django's `@login_required` decorator, so signed-out users are redirected to the login page.

---

## Acknowledgements

This project was built as part of [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/), taught by **Brian Yu** and **David J. Malan** at Harvard University. The project specification and distribution code (including the base project setup, the `User` model, and the authentication views) are provided by CS50.

---

## Built With

- [Django](https://www.djangoproject.com/): web framework
- [Bootstrap 4](https://getbootstrap.com/docs/4.4/): responsive layout and components
