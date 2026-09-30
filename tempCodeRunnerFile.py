class ottsub :
    def __init__(self, id,plan,totalamount):
        self.id = id
        self.plan = plan
        self.totalamount = totalamount
    def subcribe(self):
        print(f"Subscription ID: {self.id}, id subscribe from Plan: {self.plan}")
    def unsubscribe(self):
        print(f"Subscription ID: {self.id}, id unsubscribe from Plan: {self.plan}")
class premimumsub(ottsub):
    def __init__(self, id, plan, totalamount, premiumfeatures):
        super().__init__(id, plan, totalamount)
        self.premiumfeatures = premiumfeatures
    def premium_subscribe(self):
        print(f"Subscription ID: {self.id}, id subscribe from Plan: {self.plan} with Premium Features: {self.premiumfeatures}")

netflix=ottsub(1,"Basic",432,"full access")
netflix.subcribe()
