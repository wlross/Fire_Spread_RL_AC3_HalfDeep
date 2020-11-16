# Fire_Spread_RL_AC3_HalfDeep

# "Being the fire"

The 2020 fire season in the western United States has been among the most memorable in recent memory. With 31 fatalities and a record-breaking 4 million acres scorched, communities across California are optimistic this year remains an outlier. Yet with 7/10 of the most destructive wildfires in California history occurring in the last five years, it has become clear that communities must be prepared for resilience in the face of these events.

# Background

Among the most important entities in ensuring resilience to the increased frequency and severity of wildfire in California is Cal Fire. Through the Spring of 2020, I had the good fortune to get to know this organization through Stanford's Big Earth Hackathon and was able to extend my work on 'Project Firesafe' over the summer, supported by the Stanford Data Science Institute.

During this time, it became apparent that the ability to predict the spread of fire in real-time was critically important to response, containment, and evacuation efforts. Existing models had two faults, however.

First, many fire-spread models still relied on the 'Rothermel Surface Fire Spread Model', a physical model for fireline intensity dating back to 1972. While this model remains effective, real-world examples have made clear it's limitations.

Second, models that incorporated richer data and machine-learned approaches were often controlled by for-profit companies. As a result, Cal Fire and other fire fighting entities struggled to integrate these models into more meaningful applications used in the field.

In September of 2020, I set out to see if I could make progress towards a machine-learned fire model that went beyond the limitations of existing physical models in hopes that I would be able to share the work with the broader community.

# Prior Work

In thinking through various approaches for machine learning fire spread characteristics, I was fortunate to encounter the work of Sriram Subramanian and Mark Crowley from the University of Waterloo. This team had previously used spatial Reinforcement Learning to model the behavior of wildfires in the context of the 2016 Fort McMurray fire in Alberta Canada. To do this, they had made use of 30m resolution Landsat 7 imagery.

Reinforcement learning is effectively a computational implementation of Pavlovian conditioning where in an "agent" is allowed to take an "action" given and underlying "state". If the action results either immediately or, at a later time-step, in a positive outcome as defined by the algorithm, a "reward" is propagated to each "state-action pair" that led up to that positive outcome. Think of this as the food given to a dog each time a bell is rung, with the state being whether or not the bell is ringing. Over time, the dog learns to come when the bell is ringing because it is given the reward of food.  This is it's "policy".

Reinforcement Learning approaches are often used for 'control' style processes where, in the presence of some stochastic event (e.g., wildfire), an entity - say, Cal Fire - can assess the merits of different decisions in how to deploy scarce resources such as fire retardant or evacuation support. Subramanian and Crowley's research takes a different approach. Rather than helping an entity like Cal Fire make decisions, they make the "wildfire itself an agent" whose potential "actions- spread or not spread" are determined based on "rewards observed from historical fire boundaries".

Because the reward is pre-determined, the problem can consequently be defined as an Actor-Critic Reinforcement Learning function where the reward is propagated to the "state-action" pairs that make up the "policy" immediately following each "action - spread or not spread" event.

The great question in the formulation of this reinforcement learning problem becomes, what is the state of a fire and its surrounding area at any given point in time? And this is the geo-spatial question we sought to define.

By combining historical fire-spread boundaries from GeoMac, 3m resolution satellite imagery from Planet, historical NOAA wind speeds, topological information from the USGS, and topologically localized wind speeds obtained through the USFS's WindNinja software, we were able to establish a feature-rich state space for training our actor-critic fire spread model.

# Building the Environment

The first step to establishing the actor-critic method hypothesized was to establish the "ground truth" historical fire boundaries that would serve as the reward function. Via GeoMAC, I obtained .shp files for how the 'Camp Fire' evolved in November of 2018.

Once the fire spread boundary was in place, the next step was to layer in topology.  Through the USGS, I was able to obtain raster data for topology.  In the case of the Camp Fire, this shows how the fire spread primarily downhill into Paradise, CA.  

Absent wind, fire typically spreads uphill. Historical wind data is available via NOAA but one issue with this data is that it is collected only where weather stations are physically located. In the case of most wild fires, hyper-local wind characteristics are often critical to determining the rate of spread. Using the USFS's Conservation of Mass and Momentum solver (aka "WindNinja"), we were able to interpolate NOAA's historical wind readings and the USGS topology data to extract hyper-local wind speeds. This data helped show how despite sustained winds in the ~20mph range, the underlying topology north-east of Paradise, CA caused winds as high as ~50mph as wind rushed over ridges and mountain tops driving spread at an unprecedented rate and pace into the valley below.

In addition to topology and wind speed, the "fuel" a fire consumes is an important part of its spread.  One approach to modeling these characteristics is to parameterize and measure characteristics such as land cover and vegetation.  Rather than this approach, I elected to directly incorporate 3m resolution obtained via Planet's Planetscope Orthotile Analytic product.  This gave the model visibility at 3m resolution in the red, blue, green, and infrared characteristics of ground-cover in the area of the Camp Fire in the days prior.  

Together, these layers -- fire boundary, remote sensing data, wind speed data, and topology provided a holistic view of the three critical pillars of fire behavior -- Heat, Oxygen, and Fuel. 

Layered all together, this dataset represent an environment through which our agent -- wildfire -- could learn about it's own behavior based on this historical behavior.

# Grid and Bear It!!!

With all of the components of the model environment defined, we now needed to define a mechanisms through which behavior could be learned. In Subramanian and Crowley's original study, they had made use of a "coarse grid" where the wildfire/agent's "actions- spread or not spread" were defined as a series of 4 choices at each boundary cell for the current fire -- up/down/left/right.

By simplifying the polygons of our original boundaries into a grid, using a nearest neighbors approach for wind speeds and dividing our raster into smaller subsections of itself, each grid was defined as it's own individual "state". I allowed our original Naive fire to burn across the landscape making spread or not spread decisions at each time step and rewarded the agent for actions consistent with the historical boundary as well as penalized the agent for poor choices.

Rather than implementing a Deep-Q approach as in the original paper, I decided to implement a "Half Deep" Q learning approach that used slope, wind speed, wind direction, and burnability as the state with actions defined as burn/spread or don't burn/not spread as the action space.

Burnability was determined using the underlying rasters for infrared and RGB bands and a five layer neural network. This network was independently trained and demonstrated 83% holdout accuracy.

# Results

After allowing our algorithms to run over thousands of training cycles, our method eventually converged to a policy that demonstrated 76.3% accuracy on modeling the spread of the Camp Fire. These results were roughly in line with the results of the Crowley et al. study which showed performance ranging from 50.8-90.1% across a variety of Q-learning and Actor-Critic methodologies.

# Conclusions + Next Steps

This project represented a significant implementation bridging the fields of Reinforcement Learning, Remote Sensing, and Geospatial Informatics. In the extent it broadly expanded my own personal knowledge of RL, actor-critic methods, remote sensing data, GIS, and the intersection of physical/parametric and learned/non-parametric models, it was a marked success.

Moving forward, this work could be improved through:
-less parameterization to derive a more complex state space and improve performance
-the use of a Deep Q value function as in the original Crowley et al. paper
-the implementation of a fully convolutional approach across planet, wind, and elevation raster data
-the potential application of Bayesian methods that make use of a strong physical prior derived via Rothermel to accelerate training

