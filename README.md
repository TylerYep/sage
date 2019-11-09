# sage
CS 398 Final Project
By Tyler Yep, Jesse Doan

# Motivating Question
How can we measure a student’s growth in Hour of Code? Can we find the moments when the student has learned, or in other words, advanced to a greater ability?

Based on our predicted student ability, we can better place students in the zone of proximal development, and can then give better recommendations (feedback/next problem to try). We can also evaluate students via a different metric (grit rather than recall).

# Method
For each problem in Code.org, we can build a rubric of mistakes the students are making. Given these rubric items, we can see whether the same students stop making these mistakes on a later problem, implying some measure of growth. If we identify this change in ability, we can make informed recommendations to increase the amount / rate of learning.

# Steps
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

