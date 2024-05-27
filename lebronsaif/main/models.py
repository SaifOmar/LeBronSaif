from django.db import models
from users.models import CustomUser
from datetime import datetime


# now = datetime.now()





class Followers(models.Model):
    follower = models.ForeignKey(CustomUser,related_name="follower",on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser,related_name="followed",on_delete=models.CASCADE)
    
    
    # follows the person using his id and the followed id and the user as the follower id
    def follow(self,follower_id,followed_id):
        Followers.objects.create(follower=follower_id, followed = followed_id)
        
    # same as follow but unfollow
    def unfollow(self,follower_id,followed_id):
        obj = Followers.objects.filter(followed_id).get(follower_id)
        obj.delete()
        
        

    # gets all instances where the user if in the followed column and returns a queryset with all of these instnaces
    def get_my_followers(uid):
       
        q=  CustomUser.objects.filter(follower__followed = uid)
        return q
        
    
    def get_my_followed(uid):
        
        q =  CustomUser.objects.filter(follower__follower = uid)
        return q
        
    
    def count_my_followers(uid):
        query = Followers.objects.filter(followed = uid)[:100]
        number_of_follower =query.count()
        return number_of_follower

    def count_my_followed(uid):
        query = Followers.objects.filter(follower = uid)
        number_of_followed = query.count()
        return number_of_followed
    








    
    # def get_follower(self,uid):
    #     return CustomUser.objects.get(pk=uid)
    
    # def get_followed(self,uid):
    #     return CustomUser.objects.get(pk=uid)





class LeBrons(models.Model):
    lebron = models.TextField(null=False,blank= False, max_length=400) # tweet body
    image = models.ImageField(blank=True,null=True) 
    time_lebroned = models.DateField(null=True,blank=True)   # time craeted
    comments = models.TextField(max_length=200,null=True,blank=True)     
    passes = models.PositiveIntegerField(default=0,null=True,blank=True) # retweets
    dunks  = models.PositiveIntegerField(default=0,null=True,blank=True) # likes
    # author of the tweet (tweeter/poster)
    lebroner = models.ForeignKey(CustomUser,related_name="lebroner",on_delete=models.CASCADE) 
    
    
    
    def __str__(self):
        return f"{self.lebroner} : {self.time_lebroned}"

# comments should be changed to their own class (table) where each instance is related to the original tweet
# replies to comments should have their own class too






