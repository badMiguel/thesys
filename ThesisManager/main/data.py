class Thesis:
    def __init__(self, topic_number, title, campus, course, category, supervisor, description):
            
        self.topic_number = topic_number
        self.title = title
        self.campus = campus
        self.course = course
        self.category = category
        self.supervisor = supervisor
        self.description = description 
        
    def __str__(self): 
        return str(self.topic_number) +  ' - ' + self.title 
        
def create_thesis():
    topics = []
    
    campuses = ['Casuarina', 'Sydney', 'External']
    area = {
        'chemical': 'Chemical Engineering',
        'civil' : 'Civil and Structural Engineering',
        'electrical' :'Electrical and Electronics Engineering',
        'mechanical' : 'Mechanical Engineering',
        'computer' : 'Computer Science',
        'cyber' : 'Cyber Security',
        'data' : 'Data Science',
        'information' : 'Information Systems and Data Science',
        'software' : 'Software Engineering',
        } 
    categories = {
        'artificial' : 'Artificial Intelligence, Machine Learning and Data Science',
        'biomedical' : 'Biomedical Engineering and Health Informatics',
        'cyber' : 'Cyber Security',
    }
    supervisor = ['Bharanidharan Shanmugam', 'Yakub Sebastian', 'Sami Azam', 'Asif Karim']

    topics.append(Thesis(
        topic_number=1,       
        title= 'Machine learning approaches for Cyber Security',
        campus = campuses,
        course= [area['computer'], area['software']],
        category= categories['artificial'],
        supervisor= supervisor[0],
        description='As we use internet more, the data produced by us is enormous. But are these data being secure? The goal of applying machine learning or intelligence is to better risk modelling and prediction and for an informed decision support. Students will be working with either supervised or unsupervised machine learning approaches to solve the problem/s in the broader areas of Cyber Security.'
    )) 
     
    topics.append(Thesis(
        topic_number= 9,
        title= 'Informetrics applications in multidisciplinary domain',
        campus= campuses,
        course= [area['computer'], area['cyber'], area['data'], area['information'], area['software']],
        category= categories['artificial'],
        supervisor= supervisor[1],
        description='Informetrics studies are concerned with the quantitative aspects of information. The applications of advanced machine learning, information retrieval, network science and bibliometric techniques on various information artefact have contributed fresh insights into the evolutionary nature of research fields. This project aims at discovering informetric properties of multidisciplinary research literature using various machine learning, network analysis, data visualisation and data wrangling tools.'
    ))
     
    topics.append(Thesis(
        topic_number=16,
        title='Development of a Virtual Reality System to Test Binaural Hearing',
        campus=[campuses[0], campuses[2]],
        course=[area['electrical'], area['computer'],  area['software']],
        category=categories['biomedical'],
        supervisor= supervisor[2],
        description='A virtual reality system could be used to objectively test the binaural hearing ability of humans (the ability to hear stereo and locate the direction and distance of sound). This project aims to design, implement and evaluate a VR system using standard off the shelf components (VR goggle and headphones) and standard programming techniques.'
    ))
    
    topics.append(Thesis(
        topic_number=41,
        title='Current trends on cryptomining and its potential impact on cryptocurrencies',
        campus=campuses,
        course=[area['computer'], area['cyber'], area['software']],
        category= categories['cyber'],
        supervisor= supervisor[2],
        description= "Cryptomining is the process of mining crypto currencies by running a sequence of algorithms. Traditionally, to mine new crypto coins, a person (or group of people) would buy expensive computers and spend a lot of time and money running them to perform the difficult calculations to generate crypto coins. Some website owners have started taking a different approach; they have put the software which runs those difficult calculations into their website's Javascript. This then causes the computers belonging to the visitors of their website to run those calculations for them, instead of running them themselves. In other words, when you visit a website with an embedded crypto-miner in it, your computer and electricity is used to try to generate crypto-coins for the owners of that website. Although there are various measures being applied to stop these illegitimate minings, the trend is still increasing. This research aims to find out potential gaps in current methodologies and develop a solution that can fulfil the gap. It also aims to find out: (1) What type crypto mining methodologies are being applied?, (2) Apart from crypto-mining, what other security risks may it introduce? For example: cryptojacking,  and (3) How current web standards are tackling this problem?"
    ))
    
    topics.append(Thesis(
        topic_number=176,
        title='Artificial Intelligence in Health Informatics',
        campus= campuses,
        course= [area['electrical'], area['computer'], area['data'], area['software']],
        category= categories['artificial'],
        supervisor= supervisor[3],
        description='The project aims to use multiple publicly available health datasets to formulate a different dataset that may have features from the original set along with new ones developed through feature engineering. The dataset will then be used to build predictive model based on both general and deep learning based algorithm. The findings will be analysed and compared to similar research works.'
    ))
    
    topics.append(Thesis(
        topic_number= 180,
        title='Unsupervised Model Development from Autism Screening Data',
        campus= campuses,
        course= [area['electrical'], area['computer'], area['data'], area['software']],
        category= categories['artificial'],
        supervisor='Asif Karim',
        description='The proposed system will present a two-cluster solution from a given dataset which will group toddlers based on multiple common medical traits. In depth literature survey of similar studies, both supervised and unsupervised will be carried out before the cluster-based model is implemented. The solution will be validated using both External and Internal validation measures and statistical significance tests.'
    ))    

    topics.append(Thesis(
        topic_number= 226,
        title= 'Applying Artificial Intelligence to solve real world problems',
        campus= campuses,
        course= [area['chemical'], area['civil'], area['computer'], area['cyber'], area['data'], area['electrical'], area['information'], area['mechanical'], area['software']],
        category= categories['artificial'],
        supervisor= supervisor[0],
        description='Artificial Intelligence has been used in many applications to solve certain problems through out the academia and the industry – from electricity to writing text. AI has a multitude of applications and this project will pick up a problem and explore the applications of AI with minimal human intervention. Examples of applications include -building a bot, predicting the power usage, spam filtering and the list is endless.'
    ))    
    
    return topics

def save_new_thesis(data):
    with open('data.py', 'a') as file:
        file.write(f"save_new_thesis({data})\n")