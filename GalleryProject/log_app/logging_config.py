import logging

###
#
#try:    
   
#except Exception as e:
#   logging.error("Stripe invoice create operation failed: %s", str(e))
#   return redirect('issue-backend', e=str(e))
###




logging.basicConfig(
    level=logging.ERROR,
    filename='error.log', 
    format='%(asctime)s [%(levelname)s]: %(message)s',
)