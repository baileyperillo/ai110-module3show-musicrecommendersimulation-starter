# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**musicRec 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The intended use it to recommend music based on the user's history of musical choice and similar users. It can generate music and their ratings based on our system. You could be happy, and you can get the music to release that energy. If you're just vibin, we can recommend some easy tunes to not rec your mood. Even if your feeling some intense emotions, we could recommend music to reek havor and reck things with you. This is made for real users.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

My scoring approach is to mainly focus on the mood it gives when the user listens to it or the intended feeling, the genre of music, and the energy level it has. Though it still has the tempo_bpm, valance, dancability, and acroustic categories but it's not used in scoring at the moment. If the song matches the mood, the song will gain 3 points. If the genre is correct or similaar to someone, it recieves 3 points. If the energy levels are in a certain range of the common given song, it gets points based on it's proximity. There is also some points given based on valance, and that would be determined by prozimity to the designated standard. If I remember, a change made from the starter logic was changing point system or having mood the more important criteria. It was changed based on the suggestions given in the SHOW documentation.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset 

There are 18 songs in the catalog. There is a wide range of genres and moods. Genres can range from pop, lofi, metal, rock, jazz, electronic, synthwaves, r&b, country, folk, hip-hip, and bkues. The moods range from happy, sad, intense, angry, chill, calm, melancholic, romantic, euphoric, focus, moody, confident, nostalgic and peaceful. I added some data. I should try to find a way to make the moods less broad or put it into a group of a single word as an idea. Of course there are parts of musical taste missing in the dataset, such as era/ decade since the genre sound different with the times. There is also different languages.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

I think it does a pretty good job at recommending music, especiallt the intense music. I think there were a good amount of recommendations that were in the correct category classified.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One bias is that the application is very bias towards high- energy songs; meaning low-energy songs, like chill music, will get a much lower match. Another bias is that I chose to not give points to all the categories but it seems to affect some labelling of songs. This is especially impacting Chill Lofi music since I did not include Acousticness, Danceability, and Tempo. It doesn't help that the mood can be subjective or described differently than with a set or general word. Example being mood being melonchally or calm, not chill. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

It did not fully behave as I expected but there were a lot of fitting results. I tested user profiles:
Genre: Pop, Mood: happy, Energy: High (around 0,7)
Genre: Lofi, Mood: chill, Energy: Low
Genre: metal, Mood: intense, Energy: high

I looked at the top 5 recommended songs, looked at their genre, rating and ranking, and their reasoning.

It suprised me that a hip hop song was labelled in lofi category. All the songes in the pop category were on the low scale before adjusting. There aren't that many rock songs in the data, that a pop song was in 3rd place in intense rock.
I ran tests for weight shifting where I doubled or halfed the energy. It showed a major energy sensitivity as entries swapped places.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I want to put more priority on genre rather than mood. I might want to even make energy level a higher priority possibly. I want to include a way to make the mood category less case-sensitive. In recommendations, I want to include what categories were not matched, either it was not compatible or not counted in points. I maybe would want to consider all categories rather than just a select few. I would like to try to give a list of songs from different genres into one list for the one user.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned how to aage points of a recommendation system. I learned through going through different parts the importance of choosing the correct "algorithm" or choosing which features to prioritize. I learned that applications like this can take a lot of planning and a lot of trial and error. It was unexpected how changing small things can make such an impact or how some things are catagorized by other features, such as lofi genre being determined partially by tempo, mood, energy and such, that without them, hip-hop is considered lofi. This makes you think what do these music recommendation apps prioritize when deciding what to recommend. Do they put more emphasis on collaborative filtering or content-based? What algorithm do they use? Do they consider genre or mood more?
