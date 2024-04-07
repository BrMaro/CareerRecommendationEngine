from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegisterForm,QuestionnaireForm
from .models import QuestionnaireData,PreferredCourse
from main.models import Course
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.models import User


collaborative_filtering_model = None
content_based_filtering_model = None


# Create your views here.
def register(request):
    print("Is user authenticated:", request.user.is_authenticated)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()
        return render(request, "register/register.html", {"form": form, "user": request.user})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect("/home")
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                
    else:
        form = AuthenticationForm()
    return render(request,"registration/login.html",{"form":form})


def logout_user(request):
    logout(request)
    return redirect("/home")  


def questionnaire_view(request):
    user = request.user
    if QuestionnaireData.objects.filter(user=request.user).exists():
        questionnaire_data = QuestionnaireData.objects.filter(user=request.user)
        print(f"{request.user} data already saved")
        update_recommendation_models(user,questionnaire_data)
        recommended_courses = get_recommendations(user)
        return render(request, "register/recommendations.html", {'recommendations': recommended_courses})

    if request.method == "POST":
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form = QuestionnaireForm(request.POST)
            questionnaire_data = form.save(commit=False)
            questionnaire_data.user = user  # Associate with the current user
            questionnaire_data.save()

            print("questionnaire_data saved to model")
            update_recommendation_models(user, questionnaire_data)  # Update recommendation models

            recommendations = get_recommendations(user)
            return render(request, "register/recommendations.html", {'recommendations': recommended_courses})


        else:
            messages.error(request, 'Invalid input. Please try again.')

            return render(request, "register/questionnaire.html",{'form': form})
    else:
        form = QuestionnaireForm()
        return render(request, 'register/questionnaire.html', {'form': form}) 


def recommendations(request):
    user = request.user
    recommended_courses = get_recommendations(user)
    
    if request.method == "POST":
        locked_courses = request.POST.getlist('locked_courses')
        for course_id in locked_courses:
            PreferredCourse.objects.create(user=user, course_id=course_id)
        return redirect('register/recommendations.html')
    
    return render(request, "register/recommendations.html", {'recommended_courses': recommended_courses})




def update_recommendation_models(user, questionnaire_data):
    global collaborative_filtering_model
    global content_based_filtering_model
    
    # Update collaborative filtering model
    # collaborative_filtering_model = update_collaborative_filtering(user)
    
    # Update content-based filtering model
    content_based_filtering_model = update_content_based_filtering()

    
def get_recommendations(user):
    print("get recommendations start ")
    # collaborative_recommendations = get_collaborative_filtering_recommendations(user)
    content_based_recommendations = get_content_based_filtering_recommendations(user)
    recommendations =  content_based_recommendations # + collaborative_recommendations
    print("get recommendations end ")

    return recommendations


# def update_collaborative_filtering(user):
#     print("update_collaborative_filtering start")

#     # Retrieve preferred courses for the user from the database
#     preferred_courses = PreferredCourse.objects.filter(user=user)
#     courses = Course.objects.all()
    
#     # Prepare data for matrix factorization
#     user_matrix = []
#     for course in courses:
#         if preferred_courses.filter(course=course).exists():
#             user_matrix.append(1)
#         else:
#             user_matrix.append(0)
    
#     # Initialize and fit NMF model
#     nmf_model = NMF(n_components=5, random_state=42)
#     nmf_model.fit([user_matrix])  # Pass user_matrix as a list
    
#     print("Collaborative filtering model created:", nmf_model)  # Debugging statement
#     print("update_collaborative_filtering end")
#     return nmf_model


def update_content_based_filtering():
    # Extract user personality traits and AGP
    user_data = QuestionnaireData.objects.all().values_list(
        'conscientiousness', 'agreeableness', 'neuroticism', 'openness', 'extroversion', 'agp','age'
    )

    # Compute distances between users based on personality traits and AGP
    user_distances = euclidean_distances(user_data, user_data)

    return user_distances


# def get_collaborative_filtering_recommendations(user):
#     print("get_collaborative_filtering start")
#     global collaborative_filtering_model
    
#     # Extract preferred courses for the user
#     preferred_courses = PreferredCourse.objects.filter(user=user)
#     preferred_course_ids = [pc.course_id for pc in preferred_courses]
#     print(1)
#     # Extract all courses
#     courses = Course.objects.all()
#     print(2)
#     # Initialize user vector
#     user_vector = [1 if course.course_id in preferred_course_ids else 0 for course in courses]
#     print(3)
#     # Use collaborative filtering model for recommendations
#     user_embedding = collaborative_filtering_model.transform([user_vector])
#     recommendations = []
#     print(4)
#     # Calculate scores for each course
#     for i, course in enumerate(courses):
#         score = cosine_similarity(user_embedding, collaborative_filtering_model.components_[:, i].reshape(1, -1))[0][0]
#         recommendations.append((course, score))
#     print(5)
#     # Sort recommendations by score
#     recommendations.sort(key=lambda x: x[1], reverse=True)
#     print("get_collaborative_filtering end")

#     return recommendations[:5]  # Return top 5 recommendations


def get_content_based_filtering_recommendations(user):
    print("get_content_based_filtering start")
    global content_based_filtering_model
    
    if content_based_filtering_model is None:
        content_based_filtering_model = update_content_based_filtering()

    user_data = QuestionnaireData.objects.filter(user=user).values_list(
        'conscientiousness', 'agreeableness', 'neuroticism', 'openness', 'extroversion', 'agp','age'
    )[0]

    # Compute distances between the user and all other users based on personality traits and AGP
    distances_to_other_users = content_based_filtering_model[user.pk, :]  # Assuming user.pk is the index
    
    # Find indices of users with similar personality traits and AGP
    similar_user_indices = distances_to_other_users.argsort()

    # Exclude the user itself from recommendations
    similar_user_indices = similar_user_indices[similar_user_indices != user.pk]

    # Get top 5 similar users
    similar_users = User.objects.filter(pk__in=similar_user_indices[:5])
    print("get_content_based_filtering end")

    return similar_users
