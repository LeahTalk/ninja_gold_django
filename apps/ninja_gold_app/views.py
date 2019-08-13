from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string

import random
from datetime import datetime

def index(request):
    context = {
        "reset_display": "inline-block",
        "gold_button_display": "none",
        "title_text_color" : "green",
        "remaining_moves" : "You win!!! You are a Ninja(gambling) master!"
    }
    if ('gold_amount' not in request.session) or ('activities' not in request.session) or ('user_moves' not in request.session):
        request.session['gold_amount'] = 0
        request.session['activities'] = []
        request.session['user_moves'] = 0
    
    if request.session['gold_amount'] >= 300:    
        return render(request, 'ninja_gold_app/index.html', context)
    if request.session['user_moves'] == 15 or request.session['gold_amount'] < 0:
        context["title_text_color"] = "red"
        context["remaining_moves"] = "You lose!!! You will never be a true ninja...."
        return render(request, 'ninja_gold_app/index.html', context)
    context["reset_display"] = "none"
    context["gold_button_display"] = "inline-block"
    context["title_text_color"] = "black"
    context["remaining_moves"] = "Make 300 gold in 15 moves or less! You have " + str(15 - request.session['user_moves']) + " moves remaining."
    return render(request, 'ninja_gold_app/index.html', context)

def result(request, place):
    request.session['user_moves'] += 1
    dateTimeObj = datetime.now()
    dateStr = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day)
    timeStr = dateTimeObj.strftime("%I:%M %p")
    if place == 'farm':
        gold_earned = random.randint(10, 20)
        request.session['activities'].insert(0, {"content" : f"Earned {gold_earned} gold from the farm! ({dateStr} {timeStr})", "text_color" : 'green'})
        request.session['gold_amount'] += gold_earned
    elif place == 'cave':
        gold_earned = random.randint(5, 10)
        request.session['activities'].insert(0, {"content" : f"Earned {gold_earned} gold from the cave! ({dateStr} {timeStr})", "text_color" : 'green'})
        request.session['gold_amount'] += gold_earned
    elif place == 'house':
        gold_earned = random.randint(2, 5)
        request.session['activities'].insert(0, {"content" : f"Earned {gold_earned} gold from the house! ({dateStr} {timeStr})", "text_color" : 'green'})
        request.session['gold_amount'] += gold_earned
    else:
        gold_amount = random.randint(0, 50)
        num_sign = random.randint(0,1)
        if gold_amount == 0:
            request.session['activities'].insert(0, {"content" : f"Went even at the casino. ({dateStr} {timeStr})", "text_color" : 'black'})
        elif num_sign == 0:
            request.session['activities'].insert(0, {"content" : f"Earned {gold_amount} gold from the casino! ({dateStr} {timeStr})", "text_color" : 'green'})
            request.session['gold_amount'] += gold_amount
        else:
            request.session['activities'].insert(0, {"content" : f"Lost {gold_amount} gold at the casino! ({dateStr} {timeStr})", "text_color" : 'red'})
            request.session['gold_amount'] -= gold_amount
    print(request.session['activities'])
    return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module
    app.run(debug=True)    # Run the app in debug mode.

