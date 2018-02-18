# campus-cuckoo

A client-sided web app for the discovery of vacant classrooms on busy campuses.

## Inspiration

There have been many times in the past that, following a class, I have been
unable to find an open table or remember which classrooms are empty and for how
long. Furthermore, group projects and other small team activities often could
benefit from open spaces to work, without the hassle of reserving rooms
directly.

## What it does

**campus-cuckoo** is the interface to kilobytes of scraped data regarding which
rooms on campus are occupied either by ongoing classes or extracurricular
scheduled events.

## How I built it

Virginia Tech's [Classroom A/V Services][av] offers a wonderful yet lacking
front-end for seeing the schedule of practically every public room on campus.
While it does offer an in-depth view of activities, it can only do so one
classroom at a time. To put it in perspective, there are 140 separate buildings
representing a total of 1188 classrooms (this includes "classrooms" such as the
infamous "Animal Judging Pavilion" and "Wood Processing Lab", but nevertheless
it is a sight to behold).

[av]: http://info.classroomav.vt.edu/RoomSchedule.aspx

This data-collection aspect of this hack is powered by a series of Python
scripts that utilize `requests` and `BeautifulSoup` to probe and scrape the
schedules for every single one of these rooms (sorry!). From there, the data is
JSON encoded and trivially parsed in the browser.

## Challenges I ran into

Before coming upon the A/V services' website, I had originally scraped the
course timings from the university timetable. Inevitably, this did not
accurately represent the current status of each room by the fact that
reservations are much more flexible.

I also had expected to run into issues with the size of the data, and
especially the fact that it was going to be thrown at every browser that visits
the website. Fortunately though, this was not an issue.

## License

**campus-cuckoo** is released under the MIT license. See `LICENSE` for more
information
