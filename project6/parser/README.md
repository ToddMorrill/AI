**Sentence 3:** Do we want 'thursday' to be its own NP or should it just be a noun part of the bigger NP?
              S                              
  ____________|___                            
 |                VP                         
 |       _________|____                       
 |      |              NP                    
 |      |      ________|____                  
 |      |     |            Nbar              
 |      |     |    _________|_____            
 |      |     |   |               PP         
 |      |     |   |          _____|_____      
 NP     |     |   |         |           NP   
 |      |     |   |         |           |     
Nbar    |     |  Nbar       |          Nbar  
 |      |     |   |         |           |     
 N      V    Det  N         P           N    
 |      |     |   |         |           |     
 we  arrived the day      before     thursday

**Sentence 6:** this example should answer the question above. We *do* want noun phrases to be part of prepositional phrases, otherwise, you'd miss it entirely in this case.
                 S                 
   ______________|___               
  |                  VP            
  |        __________|___           
  |       |              PP        
  |       |           ___|_____     
  NP      |          |         NP  
  |       |          |         |    
 Nbar     |          |        Nbar 
  |       |          |         |    
  N       V          P         N   
  |       |          |         |    
holmes chuckled      to     himself

**Sentence 7:** do adverb phrases belong to verb phrases?
                                   S                                      
             ______________________|______________                         
            |                      |              S                       
            |                      |     _________|_______                 
            S                      |    |                 VP              
  __________|____                  |    |              ___|____________    
 |               VP                |    |             VP               |  
 |      _________|___              |    |     ________|___             |   
 |     |             VP            |    |    |            PP           |  
 |     |     ________|___          |    |    |     _______|___         |   
 NP    |    |            NP        |    NP   |    |           NP       |  
 |     |    |         ___|___      |    |    |    |        ___|___     |   
Nbar  AdvP  |        |      Nbar   |   Nbar  |    |       |      Nbar AdvP
 |     |    |        |       |     |    |    |    |       |       |    |   
 N    Adv   V       Det      N    Conj  N    V    P      Det      N   Adv 
 |     |    |        |       |     |    |    |    |       |       |    |   
she  never said      a      word until  we  were  at     the     door here

**Sentence 8:** Do we want conjunctions in the middle of verb phrases?
        S                                
   _____|____________                     
  |                  VP                  
  |          ________|________            
  |         |        |        VP         
  |         |        |     ___|___        
  NP        VP       |    |       NP     
  |      ___|___     |    |    ___|___    
 Nbar   VP     AdvP  |    |   |      Nbar
  |     |       |    |    |   |       |   
  N     V      Adv  Conj  V  Det      N  
  |     |       |    |    |   |       |   
holmes sat     down and  lit his     pipe

**Sentence 10:** is this the way we want to parse this? This sentence makes noun phrase chunking seem somewhat arbitrary (e.g. 'I' vs 'paint', etc.).
      S                                                                        
  ____|___                                                                      
 |        VP                                                                   
 |     ___|___________                                                          
 |    |               NP                                                       
 |    |    ___________|__________________                                       
 |    |   |                             Nbar                                   
 |    |   |            __________________|_________________                     
 |    |   |           |                                   Nbar                 
 |    |   |           |                        ____________|________            
 |    |   |           |                      Nbar                   |          
 |    |   |           |              _________|____                 |           
 |    |   |           AP            |              PP               PP         
 |    |   |     ______|____         |     _________|___          ___|___        
 NP   |   |    |           AP       |    |             NP       |       NP     
 |    |   |    |       ____|___     |    |          ___|___     |    ___|___    
Nbar  |   |    |      |        AP  Nbar  |         |      Nbar  |   |      Nbar
 |    |   |    |      |        |    |    |         |       |    |   |       |   
 N    V  Det  Adj    Adj      Adj   N    P        Det      N    P  Det      N  
 |    |   |    |      |        |    |    |         |       |    |   |       |   
 i   had  a  little moist     red paint  in       the     palm  of  my     hand