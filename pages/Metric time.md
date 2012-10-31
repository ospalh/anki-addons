title: Metric time
id: metrictime
main_file: Metric%20time.py
status: personal hobby horse, broken
type: addon
status_color: red
status_text_color: white
abstract: Shows times in some spots as days or years.
first_image: Studied%20in%20days.png
first_alt: The time studied is shown in days, not hours.

This add-on is just me riding my favorite hobby horse,
[metric time](http://en.wikipedia.org/wiki/Decimal_time#Fractional_days).
I think splitting days into hours, minutes and seconds is about as
silly as splitting lengths into inches, feet, yards, rods, chains and
miles or using pounds and ounces and stones and who-knows-what else for
mass. (Or weight. Better not go
[there](http://en.wikipedia.org/wiki/Slug_(mass))! And how much is a
[gallon](http://en.wikipedia.org/wiki/Gallon)‽)

<blockquote class="nb">
This add-on assumes that a complete Python is installed. It will not
work with just Anki installed. Specifically, it uses the decimal
module, which is part of the Python standard library, but not included
with Anki.
</blockquote>


This add-on replaces the standard time-formatting function with one
that returns times shorter than a year as days – even times much
shorter than a day. Longer times are written as years with one decimal
place.

### AnkiDroid
Daring spirits can use my
[variant](https://github.com/ospalh/Anki-Android/tree/metric-time) of
[AnkiDroid](https://github.com/nicolas-raoul/Anki-Android). I have
added the equivalent of this addon, showing times as fractional days in
AnkiDroid. You should merge this branch into the newest version of
AnkiDroid, not just use that branch as-is.
