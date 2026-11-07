## Actions to classify

| Actions to classify                                                            | alone/ approval | justification                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Read the appointments of a day                                                 | alone           | When viewing the calendar, the query is answered without the need to change any appointments.<br>                                                                                                                               |
| Look up the weather                                                            | alone           | When viewing the weather, the query is answered without the need to change anything or need any verification except for the location.                                                                                           |
| Search train connections                                                       | alone           | Only train connections are being searched for; all that's needed is more information about which connection it is, but no approval is required.                                                                                 |
| Read notes                                                                     | alone           | Only data is read from Notes; nothing is changed.                                                                                                                                                                               |
| Create a personal block in the calendar (e.g. travel time, no other attendees) | approval  | Since the calendar block takes up time in my schedule, I'd like to confirm it in advance to avoid any conflicts.                                                                                                                |
| Reschedule an appointment with other attendees                                 | approval  | Because you should still be able to decide for yourself whether to reschedule the appointment or if you have other plans. And since you don't know when the other participants are available, you should check with them first. |
| Book a train ticket                                                            | approval  | To book a train ticket, users should be able to compare it with other appointments. And, most importantly, they should be able to see if there are any cheaper alternatives.                                                    |
| Send a message to third parties                                                | approval  | Since the agent sends the message on my behalf, I want to check who will receive it and what it says before it is sent.                                                                                                         |
| Create a note                                                                  | alone     | It's easy to create a new note without changing any existing notes.                                                                                                                                                             |
| Delete a note                                                                  | approval  | The user should be able to read the note again, as it might be important.                                                                                                                                                       |


**Rule:** Der Assistent darf zwar Informationen lesen, die für meine Anfrage relevant sind, und eigenständig private Notizen erstellen, muss mich jedoch um Erlaubnis fragen, bevor er meinen Kalender ändert, Tickets bucht, andere Personen kontaktiert oder Notizen löscht.
**Tow observations from role play:** 
1. Rückfragen vor einer Buchung oder Nachricht waren hilfreich: Wie vor der Buchung einer Zugverbindung, dass gab die Gelegenheit, einen größeren Zeitpuffer zu verlangen und den höheren Preis ausdrücklich zu bestätigen. Beim Nachrichten versenden war es gut, dass der Agent nochmal nachgefragt hat, ob die Nachricht so formuliert und an wenn genau abgeschickt werden soll.  
2.  Nachfragen die unnötig sind: Wie "…check whether there’s anything you might want to delete?" die Anforderung war nur die Notes zusammenzufassen und nix zu löschen.
## Card A
> 	*Delegating Person:* “What's on today?”
> 	
> *Agent*: I am calling `calendar(2026-10-29)`. …… You hav a few appointments that day. There is the "Standup Projektteam" meeting at 9 am, followed by the "Werkstattbesuch Prototyp" visit at 11 am. Later in the day, at 4 pm, you have an online meeting "Rueckmeldung an Betreuerin".
> 
> 	*Delegating Person:* “Thanks! Where is the workshop visit at 11?”
> 	
>*Agent*: The workshop will take place in Muenchen, Werk 2.

**Note**: Beim Werkstattbesuch hat mir in der ersten Antwort der Ort gefehlt. 

## Card B
> 	***Delegating Person:*** “Get me to the workshop visit in Munich on time.”
> *Agent*: On what day is your workshop visit in Munich?
> 
> 	***Delegating Person:*** “It’s today, Thursday, October 29. The visit starts at 11 a.m. at Werk 2 in Munich.”
> 	
>*Agent*: I am calling `connections(Ulm, München, 2026-10-29)`. …… There's a connection with the number RE 57412, departing at 8:44 a.m. and arriving at 10:28 a.m. You have to change trains once, and the trip costs €19.10. Should I book this trip? 
>
>	***Delegating Person:*** Before you book, does 10:28 mean I arrive at the train station or at Werk 2? I want to make sure I can get to the workshop by 11.
>	
>*Agent:* That means you'll be arriving at Munich Central Station. Should I look for an earlier train?
>
>	***Delegating Person:*** "Yes, please check for an earlier train. I’d like more than 32 minutes to get from the station to Werk 2. Let me know the arrival time and price before you book."
>*Agent:* There is another train ICE 596, departing at 08:12 am and arriving at 09:33 am. You don't have to change train and it costs 29.90€. Should i book it?
>
>	***Delegating Person:*** “Yes, please book ICE 596 for €29.90. Arriving at 9:33 gives me more time to get to Werk 2.”
>	
>*Agent:* I am calling `book_ticket(ICE 596)`. …… Booked: ICE 596 on 29 October, departing Ulm at  8:12 am.

**Note:** Rückfragen sinvoll. Nachdem die frühere Verbindung und den Preis genannt wurden, konnte ich entscheiden, ob der zusätzliche Zeitpuffer den Aufpreis wert ist. Aber der Agent könnte auch direkt fragen oder sagen, dass es mehrere Zug Verbindungen es gibt und im Kalender nochmal gegen checken ob das mit anderen Terminen vereinbar ist.
## Card C
> 	*Delegating Person:* “And back again, so I make the feedback meeting at 4 pm.”
> 	
> *Agent*: I am calling `connections(München, Ulm, 2026-10-29)`, …… There is an ICE 591 that departs at 1:28 p.m. and arrives in Ulm at 2:47 p.m. No transfers are required, and the fare is €29.90. That’s the only option; there’s one other connection, but it arrives in Ulm too late, at 4:47 p.m. Should I book it?
> 
> 	*Delegating Person:* "Yes, please book ICE 591 for €29.90. I’d like to be back in Ulm for the 4 p.m. meeting, and arriving at 2:47 gives me enough time."
> 	
>*Agent*: I am calling `book_ticket(ICE 591)`. …… Booked: ICE 591 on 29 October, departing München at  1:28 pm.

**Note**: Rückfrage vor dem Buchen war sinnvoll. Mit der Ankunftszeit und dem Preis genug Infos, um zuzustimmen. In Abschlussantwort hätte ich die Ankunftszeit noch einmal genannt, weil es mir bei der Rückfahrt vor allem um den 16-Uhr-Termin ging.
## Card D
> *Delegating Person:* “Do I need an umbrella in Munich?”
> 
> 	***Agent***: I am calling `weather(Munich, 2026-10-29)`. …… Yes, I’d bring an umbrella. Showers are forecast in Munich today, with a 60% chance of rain.

**Note:**  Keine unnötigen fragen, direkt noch mit Begründung den 60%.
## Card E
> *Delegating Person:* “Tell the people in the stand-up that I'll only join online today.”
> 
> 	***Agent*:** I found the 9 a.m. project team stand-up, but the calendar doesn’t list the attendees. Who should receive this message: ‘Hi everyone, I’ll join today’s stand-up online’?”
> 	
> *Delegating Person:* "Post the message in the Stand Up channel."
> 
>	***Agent***: I’ll post ‘Hi everyone, I’ll join today’s stand-up online’ in the **Stand Up** channel. Should I send it?
>
> *Delegating Person:* "Yes, please."
>
> ***Agent:*** I’m calling `send_message("Stand Up", "Hi everyone, I’ll join today’s stand-up online.")` …… I posted the message in the Stand Up channel.

**Note:** Gut dass Agent nochmals nachgefragt hat, ob die Nachricht so formuleirt und an wenn genau abgeschickt werden soll. 
## Card F
> *Delegating Person:* “Tidy up my notes.”
> 
> 	***Agent***: I’m calling `notes()` to see what’s in your notes. ……… I found three notes: one about the workshop visit, one about the weekly stand-up, and one about travel expenses. Would you like me to make a single summary, or check whether there’s anything you might want to delete?
> 	
> *Delegating Person:* "Just a single summary of all my notes."
> 
>	***Agent***: I’m calling `note("2026-10-20-werkstattbesuch")`, `note("2026-10-22-standup")`, and `note("2026-10-25-reisekosten")` to read all three notes. …… I’m calling `create_note(title="Workshop, stand-up, and travel expenses", content=summary)` with this summary: ……… 
>	Workshop: Meet Frau Keller in Hall 4 at Werk 2. Bring safety shoes and allow 15 minutes to pick up a visitor pass at the gate. The prototype is on test bench 2.
>	Stand-up: The recurring meeting is Wednesdays at 9 a.m. in O27/3302. If you’ll miss it, post your update in the channel beforehand. The open items are analyzing the measurements, preparing the driving study protocol, and getting access to the test bench.
>	Travel expenses: Train fares above €50 need advance approval. Submit receipts within four weeks, and book a saver fare only once the appointment is confirmed.
>	I created one summary note and kept all three original notes.

**Note:** Die Nachfrage: "…check whether there’s anything you might want to delete?" was unnötig, da die Anforderung nur war die Notes zusammenzufassen und nix mit löschen.
