**Motivation**

Fast-paced world of teen culture really took me by surprise with the upraisal
of teen aesthetic genres. 

I find myself too old to be able to distinguish between
"draincore", "weirdcore", "breakcore", "glitchcore" e.t.c but really don't 
want to lose my face among the youngsters being unable to distinguish between
two anime-style blurry pictures. That's why I was in heavy need of an assistant
to help me classify those.

Meet the Corephaeus.

**Capabilities**

Model was trained to classify 4 different aforementioned aesthetics, 
however you can very well have fun with it by asking to classify an
image of your dog.

You can visit @corephaeus_bot telegram bot to try it out.

**Model**

Network is built upon VGG16 classifier and uptrained for my needs.
A notebook with the model can be also found in the repo.

**Data**

Data was collected from Pinterest. Around 1500 images of different genres 
were collected and manually processed in total. Image used to collect
the data can be found at https://github.com/kol-di/CoreScraper.

**Worth mentioning**

I was initially so confused by these teenage aesthetic genres, that actually
incorrectly attributed to "breakcore" as one of them. In deeply theoretical
meaning (if there is one), it is a music genre and is not supposed to have a
distinguishable visual style. This is clearly seen in a rather bad model performance
classifying breakcore, compared to other styles

But I am pretty sure, that it has certain visual features, so classification of this genre
is still possible to a certain degree. All after all, this is how culture emerges - 
from nowhere comes something, and suddenly a new genre arises.

