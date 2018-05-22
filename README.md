### ECE-143-Indiviual-Project
[How to use markdown, remember to remove](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
README file for individual project

Author: Joy Nwarueze
Electrical Engineer Undergraduate

#### discussions on the problem:
This is what I took away from reading the prompt: 

- A user will define the region, you must fill it with random (size and location) rectangles.

Now luckily, I wrote down my thoughts on what conditions should consider when making the rectangles. It's a pretty sparse list since it was based on the steps I made for myself as I worked through it.

###### Conditions:
 * Q. What if the Tower is larger than the region or partially in/out of region?
     A. Limit the max coordinates of x0,y0,x1,y1 generated by randint. Namely x0 can go from 0->X-1 and y0 from 0->Y-1. Why -1 and not just X and Y? x1 and y1 need to appear somewhere in the region so I don't have to deal with a x0 = max range(X) and y0=max range(Y)
 * Q. What if a tower is enclosed entirely in a previously established region?
     A. This was a hard one. Mostly that it was hard to detect as it didn't violate an edge of a previously established rectangle but my function could still detect that an overlap was occurring. I first noticed it when the program would try to reference something that wasn't established because it wasn't trimmed and therefore assigned to a Tower instance. Once I could consistently find that encompassed rectangle, I couldn't delete it, but I also didn't want it's area adding to the total covered area. So I essentially collapsed it to a single point with no depth. That means it's area would be zero.
 * Q. How will I store the information of each tower?
     A. Structs!... wait...does Python have structs?... Google says no. Alright I'll just use dictionaries that store the tower and it's information. But that seems like a lot of work. So I asked a friend in the class what he did. He made a Tower class. Genius. So yeah I ended up with a Tower class that has a settable index so it can be indexed in a dict I did ultimately create. However that dict stores the index (an integer) as a string so it'll be an immutable key, and the Tower itself was the stored "value".
   * Q. How many Towers is too much?
     A. I did a 10 by 10 grid that kept going as long as there was space. That took 65 towers to finish. Keep in mind that at some point a lot of these towers were overlapping and had to keep checking against all other towers previously made. An arbitrary limit that seems reasonable is the limit used on hash maps before they resize which I believe is 75%. Why such an arbitrary limit? If this was applied to the real world, I wouldn't be too happy with seeing 20 towers between my walk from The Village to Price Center.
     
#### trade-offs:
ImageDraw vs Numpy:

ImageDraw:
    Pros:
        + Simple to code
        + Satisfying shapes
    Cons: (might be due to inexperience with it)
        - Misleading plotting on a graph
        - Outlines are huge. To the point where it was distracting. So I removed them
   
Numpy:
    Pros:
           + I ended up using numpy arrays to convert ImageDraw region to a plot
           + probably a lot more accurate
    Cons:
           - Worked on Numpy Shapes right before starting this. Frustrated me to the point of vehemently avoiding using it again.
           - Would probably have to do a lot more research to create my region and rectangles. Not really a bad thing, but I was on a time crunch


#### limitations details:
Limitations of ImageDraw:
* Region: 
    The X range can actually be sized under 4 units and Y range under 5 units, however the background image plot gets weird. What I mean is that by using ImageDraw rectangles would show up in the negatives even though their coordinates specified that they are above 0. 
* Pixels:
    The coordinates don't align neatly with the plot axis because ImageDraw works by pixels rather than exact integer values. This could lead to a lot of misunderstanding when viewing the plot trimming a rectangle. You'll see that after a trim, the plot will still show a little overlap before being added to the superset of towers. However it has been trimmed correctly, it's just not as good at showing it. Also, when towers look like they clearly overlap on the plot and then don't trim are actually not overlapped. That caused me a lot of stress redrawing the plot by hand of the 2 conflicting or non-conflicting rectangles and wondering what in the world is happening. In short, ImageDraw may not be the best source when it comes to precision images. If I could convert from ImageDraw to Numpy, I'm certain it would look a lot more accurate. And I could add outlines that aren't an affront to the eyes.
* Trimming:
    Each trimming shown consequetively based on collision detection order. So you might see a polygon rather than a rectangle, but rest assured it's not finished trimming until its grayed in. 
   


#### analysis:
Now a big question is: How can I make the output user friendly? If I was given a rectangle maker, what would I want to know?
* How many Rectangles are on this plot?
* How much of the plot is currently covered?
* How many wildly different rectangles would be needed to fill a region I define (on average preferably)?
To me, being able to convey answers to these questions either through output or pictures would make this a complete project. However, I must be mindful of what I can complete in the time given to me such that I don't try to add so much that I don't finish in time. 

Here is a list of Steps that I used to solve this problems in consideration of the conditions stated earlier:
- Step 0: Make a plot
- Step 1: Make a rectangle of height, width (but need a plot first)
- Step 2: Randomly generate the sizes of the rectangles that fit in the region
- Step 3: Store data on the rectangles so the shape can be changed and a "new" rectangle can replace it
("new" here means white out the conflicting new rectangle, recolor in the trimmed rectangle, then use the superset rectangle to recolor the overlapped area back to gray)
- Step 4,5: Trim overlapped rectangles. Maybe make a dummy rectangle or use the superset rectangles (the one I went with)
- Step 4.5: Detect overlaps and how many overlaps (Took 1 full day - By far the most difficult part)
- Step 5: Actually trim a Rectangle. (This is where the aggressive amounts of handwritten plotting and double-checking everything went into. Many comparisons were added at this step based on what I could write down and understand. The "New rectangle completely encompassed by superset" was the rarest and most confusing condition to address.
- Step 6: When to actually draw each rectangle and show it. At this point I had too many "show plot" sequence of codes scattered around my code. I created one method for that and retroactively removed some of the previous sequences to avoid getting duplicate plots. So many duplicate plots... Python yelled at me for having to many....
- Step 7: Progress bar. I wasn't going to plot an actual bar because I don't have time for that but then again it might be really simple. However I think simple print statements keep things from being too cluttered.
Step 8: Stop coding and document/populate info. I still did some coding to fix the imaging but today (5/21/18) was dedicating to documentation.

#### good visualizations:
 - Are my plots good? No outlines for the rectangles unfortunately, ImageDraw makes it look weird.
 
 
## Conclusion:
I hope this was a helpful read on how I thought through this problem. It might not have been clear but a main focus on mine was modularization and clarity of code. A recent coding project I worked on made me realize how unclear my variables look to someone who has no clue what my code is meant to do. I'm still practicing and I feel in the future, actually planning out my starting variable names might help me get in the right mindset.  