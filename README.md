# drugs-embedding

## Project goal: 
find drug(molecule) combinations that can be used for new diseases (i.e. other than the purpose of each molecule taken separately)
## Example:  
'nifedipine': high blood pressure, 'lidocaine': local anesthetic, 'nifedipine+lidocaine': hemorrhoids treatment 

## Steps:
* Find a good embedding model for drugs and diseases
  ** How to evaluate if a model is good for drugs? Take known drugs and see of they embed close together eg. via hierarchical clustering
  ** How to evaluate if the drugs to disease embeddings is good? Ibuprofen - Fever - Lidocaine = ? Ibuprofen - Pain - Nifedipine = ? We should get the diseases
  ** we can also use, instead of 1.2., ground truth data from online resources, human curated: drugs.com. We can see if the diseases are close to the drugs
* Discover new combinations and diseases: try to combine molecules and see to which disease they are close to.
