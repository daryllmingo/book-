import pickle
import streamlit as st
import numpy as np


st.set_page_config(page_title="Book Recommender System", layout="wide")

model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
popularity = pickle.load(open('popularity.pkl', 'rb'))

st.markdown("""
    <style>
        
        body {
            font-family: Arial, sans-serif;
        }

        .header {
            font-size: 48px;
            color: #dde8a9; 
            text-align: center;
            margin-top: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); 
        }
        .s_head{
            font-size: 32px;
            color:  #94d5d6;
            text-align: center;
            margin-top: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); 
                
        }
        .img{
            padding: 20px;
            margin-top: 20px;
            text-align: center;
         }
        .css-18e3th9 {
            background-color: rgba(243, 244, 246, 0.9); 
        }
        .img1{
            text-align:center;
            margin: 5px;
            padding: 10px;

        }
        .book-title {
            font-size: 16px;
            font-weight: bold;
            color: #512f87; 
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Home", "Recommend Books", "Top Books", "Explore More"])

def top_fifty():
    book_n = popularity['b_title'].tolist()  
    authors = popularity['author'].tolist()  
    votes = popularity['v_ratings'].tolist()  
    ratings = popularity['avg_ratings'].tolist()  
    images = popularity['img_ul'].tolist()  

    return book_n, authors, votes, ratings, images

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])
    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)
    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url)

    return poster_url

# Function to recommend books
def recommend_books(book_name):
    books_list = []
    distances_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=15)

    poster_url = fetch_poster(suggestions)
    for i in range(len(suggestions[0])):
        book_title = book_pivot.index[suggestions[0][i]]
        distance = distances[0][i]
        books_list.append(book_title)
        distances_list.append(distance)
    return books_list, poster_url, distances_list

if pages == "Home":
    st.markdown('<div class="header">Welcome to the Book Recommender System</div>', unsafe_allow_html=True)
    st.markdown('<div class="s_head">Find your next favorite book! Go to the Recommend Books page to get started.</div>', unsafe_allow_html=True)
    st.markdown('''
        <div class="img"> 
            <img src="https://wordsrated.com/wp-content/uploads/2022/02/Number-of-Books-Published-Per-Year.jpg" 
                alt="sirishko phool" 
                style="width: 50%; height: auto;">
            </a>
            <h1>About Us </h1>
            <p font-size: 200px; text-align: justify;>A book recommendation system is designed to suggest books to readers based on their interests and preferences. These systems are commonly utilized by online platforms that offer eBooks, such as Google Play Books, Open Library, and Goodreads.
            With the growth of the internet, customers now have access to an extensive array of products from eCommerce sites. Finding the perfect items at the right time can be challenging. Personalized recommendation systems help users navigate this vast selection by suggesting relevant books, news, movies, music, online courses, and research articles tailored to their preferences.</p>
        </div>
        <div class="img1">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs2kdLFeByx21N0IB7_J4hQ8yZdlFWQ-p5tw&s" 
                alt="Popular Books" 
                style="width: 50%; height: auto;">
    ''', unsafe_allow_html=True)

elif pages == "Recommend Books":
    st.markdown('<div class="header">Book Recommender System</div>', unsafe_allow_html=True)
    
    selected_books = st.selectbox("Search for books", books_name)
    if st.button('Show Recommendation'):
        recommendation_books, poster_url, distances = recommend_books(selected_books)

        # Display recommendations in rows of 7
        for row in range(0, 14, 7):
            cols = st.columns(7)
            for i in range(7):
                index = row + i + 1
                if index < len(recommendation_books):
                    with cols[i]:
                        st.markdown(f'<div class="book-title">{recommendation_books[index]}</div>', unsafe_allow_html=True)
                        st.image(poster_url[index])
                        st.markdown(f'<div class="distance-info">Distance: {distances[index]:.2f}</div>', unsafe_allow_html=True)

elif pages == "Top Books":
    st.markdown('<div class="header">Top 50 Books</div>', unsafe_allow_html=True)

  
    book_n, author, votes, rating, image = top_fifty()
    
    for a in range(len(book_n)):
        st.markdown(f'''
            <div class="container">
                <div class="row">
                    <div class="col-md-3" style="margin-top: 50px">
                        <div class="card">
                            <div class="card-body">
                                <img class="card-img-top" src="{image[a]}" style="margin-top:50px">
                                <h2 class="text-white">{book_n[a]}</h2>
                                <h4 class="text-white">Author: {author[a]}</h4>
                                <h4 class="text-white">Votes: {votes[a]}</h4>
                                <h4 class="text-white">Rating: {rating[a]}</h4>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

else:
    st.markdown('<div class="header">Popular Books in Nepal</div>', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.slideshare.net/slideshow/siris-ko-phool/9090315" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Shirish_ko_Phool.jpg" 
                     alt="sirishko phool" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
            </a>
            <h2>Sirish ko phool </h2>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.scribd.com/doc/112964504/mUnA-mAdAn" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/1/1d/Muna_Madan_-_book_cover.jpg" 
                     alt="muna" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>Muna Madan </h2>
    </div>
''', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.scribd.com/doc/36891833/Karnali-Blues" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/8/86/Karnali_Blues_by_Buddhisagar.jpg" 
                     alt="karnali" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>Karnali blues </h2>
    </div>
''', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://thuprai.com/book/palpasa-cafe-english/" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/1/19/Palpasa_Cafe_by_Narayan_Wagle.jpg" 
                     alt="palpasa cafe" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
            </a>
            <h2>Palpasa Cafe</h2
            >
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.scribd.com/document/379361258/TeenGhumti" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/4/49/Teen-Ghumti-book.jpg "
                     alt="teenghumti" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>Teen Ghumti</h2
        >
    </div>
''', unsafe_allow_html=True)

    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.slideshare.net/slideshow/bhupi-sherchan-ghumne-mech-mathi-andho-manchhe/62392551" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/c/c8/Ghumne_Mechmathi_Andho_Manche.jpg" 
                     alt="ghumne" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>Ghumne Mechmathi Andho Manche </h2
        >
    </div>
''', unsafe_allow_html=True)
    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.scribd.com/document/614389748/The-Gurkhas-Daughter-Stories-Parajuly-Prajwal-Z-lib-org" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/0/0b/The_Gurkha%27s_Daughter.jpg" 
                     alt="gurkhas" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>The Gurkhas Daughter </h2
        >
    </div>
''', unsafe_allow_html=True)
    st.markdown('''
        <div style="text-align: center;">
            <a href="https://www.scribd.com/document/284770090/Narendra-Dai-by-BP-Koirala" target="_blank"> 
                <img src="https://upload.wikimedia.org/wikipedia/en/5/5e/Narendra_Dai.jpg" 
                     alt="narendra" 
                     style="width: 200px; height: auto; border-radius: 15px; margin-bottom: 20px;">
        </a>
        <h2>Narendra Dai</h2
        >
    </div>
''', unsafe_allow_html=True)