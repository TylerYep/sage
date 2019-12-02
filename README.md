# sage
CS 398 Final Project
By Tyler Yep, Jesse Doan

# Instructions
Adding more documentation because, heavens, we have guests!
Obtain the Code Studio data from Chris Piech (cpiech) and put it in `data/`.

## Data Exploration
Run `python data_loader.py` to convert the data to json.

Set `USE_FEEDBACK_NN = False` in explore.py.

Then, run `python explore.py` to examine specific data examples.

## Autograder
Jump into generate with `cd generate/`.

Run `python sample.py [problem_num]` to get training data. This will also give the top 50 submissions in the source data that were not represented in your grammar. Fix your grammar!

Run `python preprocess.py [problem_num] [data_path_here.pkl]` to convert/split the data into train/val/test.

Run `python train.py [problem_num]` to train the model.

Run `python explore.py` to examine specific data examples.


# TODO
1. Visualizing this data somehow (cluster neighbors). @Peter/Natalie/Andrew
2. Order by number of submissions?

## Milestones
- Wrote a grammar for p1-p4.
- Created data exploration tool.
- Create visualizer for rubric sampled AI.
- Anomaly Detection.
- Ability Estimation.

P1 - 82%
P2 - 99%
P3 - 51%
P4 - 56%
P9 -




# Project Info

## Motivating Question
How can we measure a student’s growth in Hour of Code? Can we find the moments when the student has learned, or in other words, advanced to a greater ability?

Based on our predicted student ability, we can better place students in the zone of proximal development, and can then give better recommendations (feedback/next problem to try). We can also evaluate students via a different metric (grit rather than recall).

## Method
For each problem in Code.org, we can build a rubric of mistakes the students are making. Given these rubric items, we can see whether the same students stop making these mistakes on a later problem, implying some measure of growth. If we identify this change in ability, we can make informed recommendations to increase the amount / rate of learning.

## Steps
1. Create rubric items for mistakes students make, and also when they don't make mistakes. This should align with intuitive notions of student growth, such as:
    * time to problem completion? (might not be true)
    * number of submissions
    * number of backtracks
    * amount of code increasing vs decreasing
    * code style?
2. Simulate a student with some ability a_{init} answering questions on all Hour of Code questions.
  * Their ability randomly grows and rubric items change, and build our dataset.
  * Zero-shot learning problem.
3. Validation - given a real student, predict student ability a_{final} using marked rubric items, and get a sense of the slope of a student's growth. See which rubric buckets change the most over time.
