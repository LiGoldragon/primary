Presentation.{ «Energy is read against the useful hours» Proposal }

# Energy is read against the useful hours

Created by Fable 5.2.

### Proposal 1: Pace counts each hour at its usefulness · psyche-belief › vision/energy-nexus-v1.md

::: comment
His words, 13 November: «Can't we get the readings to give us a time-adjusted fuel tank?» «Power is per time. So how much potential is left means how much potential per time.» «daytime and nighttime are not usually even. I can run you a lot harder in the daytime while I'm talking to you.» «if there's like X amount left, but there's only 1 day and 2 nights left, that should read differently than if there's 2 days and 1 night for the same energy.» And on the first draft of this page: «we should make the energy nexus configurable, like the time usefulness at different time of the day. Some people might want to take the weekend off, some people might have a job and do this part-time. The highest potential time is something that needs to be configurable.» The first draft configured two values and fixed in its types that every day is alike and that an hour is either attended or not. Here the schedule itself is the configuration: any hours of any weekdays, each at its own usefulness.
:::

::: shown
psyche-belief › vision/energy-nexus-v1.md
## Pace: over or under, per day
:::

- A reading alone says how much is left; pace says whether the machine is spending it as intended. Each provider has a target: Even spends the window evenly; SpendBy spends it whole by an instant, as when a Codex reset is to be redeemed before it expires and the week is meant to be used up first. Pace is the comparison of what has been used to what the target says should have been used by now, per day.
+ A reading alone says how much is left; pace says whether the machine is spending it as intended, and is the default answer to every reading. Each provider has a target: Even spends the window evenly; SpendBy spends it whole by an instant, as when a Codex reset is to be redeemed before it expires and the week is meant to be used up first. Pace is the comparison of what has been used to what the target says should have been used by now.

+ Energy is best spent in the hours it is most useful, so pace measures time in useful hours: each hour of the week counts at the usefulness its owner gave it, and an hour he named nothing for counts at the baseline. The same energy left reads lower with one day and two nights ahead than with two days and one night. Pace says how many hours the window has left, how many useful hours those come to, and what is left per useful hour: the power the machine can run at.

+ The schedule is its owner's: one who works every day, one who keeps the weekend, and one who has two evenings a week each say so in spans.

+ Where two spans name the same hour, the more specific one counts: the span naming fewer days, and between two naming as many days, the one naming fewer hours. An override counts over every span.

```ethos
+ Hours.Integer
+ Hour.Integer                         ; 0 to 23, in the owner's local time
+ Weekday.[ Monday Tuesday Wednesday Thursday Friday Saturday Sunday ]
+ Usefulness.Percent                   ; what an hour counts for; 100 is an hour at full use
+ Baseline.Percent                     ; the usefulness of an hour no span names
+ Span.{ Vector<Weekday>               ; on these days,
+        From.Hour To.Hour             ;   between these hours,
+        Usefulness }                  ;   an hour counts this much
+ Override.{ From.Instant To.Instant   ; between these two instants, whatever the schedule says,
+            Usefulness }              ;   an hour counts this much
```

+ A schedule may be drawn from the record of when its owner was most active, in place of his own estimate.

+ An override sets the usefulness of one stretch of time, over the schedule: a day away, a meeting, a morning he means to work hard. He sets one by hand; whatever keeps his calendar sets one as an entry is made, an event like any other.

```ethos
  Pace.{ Provider
         Target
-        Expected.Percent              ; what the target says is used by now
+        Expected.Percent              ; what the target says is used by now, time counted in useful hours
         Used.Percent
         Standing.[ Over Under On ]    ; used against expected
-        PerDay.Percent } ]            ; the daily share the target implies from here
+        HoursLeft.Hours               ; the hours left in the window
+        UsefulLeft.Decimal            ; those hours, each counted at its usefulness
+        PerUsefulHour.Decimal } ]     ; percent left per useful hour left
```

::: comment
The meta signal and the Memory take the schedule, one span at a time as every other value.
:::

```ethos
  Set.[ Polling.Minutes
        Threshold.Threshold            ; one level's boundary
        Reminder.Reminder              ; who hears about a level
        RemoveReminder.Reminder
        RedeemExpiring.Minutes         ; redeem within this many minutes of a reset expiring
        RedeemUsedAtLeast.Percent      ; or when the week is this used
-       Target.ProviderTarget ] ]      ; one provider's pace target
+       Target.ProviderTarget          ; one provider's pace target
+       Span                           ; one span of the schedule, added
+       RemoveSpan.Span
+       Override                       ; one stretch of time, set over the schedule
+       RemoveOverride.Override
+       Baseline ] ]                   ; the usefulness of every other hour
```

```ethos
  Configuration.{ Polling.Minutes
                  Vector<Threshold>
                  Vector<Reminder>
                  RedeemExpiring.Minutes
                  RedeemUsedAtLeast.Percent
-                 Targets.Vector<ProviderTarget> }
+                 Targets.Vector<ProviderTarget>
+                 Schedule.Vector<Span>
+                 Vector<Override>
+                 Baseline }
```

::: comment
The examples, with the new pace. The first schedule is his own as an example, every day from 8 to 22 at full use and the rest at a fifth, and the reading is his Codex week as it stood on Friday 13 November at 16:50: a quarter of the week's useful time gone, 35 used, so 10 over; 124 hours left, 83.5 of them useful, and 0.78 percent for each useful hour. The two schedules after it are other lives, as examples.
:::

```datom
+ Configure.Baseline.20
+ Configure.Span.{ [ Monday Tuesday Wednesday Thursday Friday Saturday Sunday ] 8 22 100 }
+ Read.Codex
+ Read.{ { Codex true [ { Week 35 1795054860 10080 } ] [] 1794610200 }
+        { Codex Even 25 35 Over 124 83.5 0.78 } }
+ ; one who keeps the weekend: weekdays at full use, the weekend at the baseline
+ Configure.Span.{ [ Monday Tuesday Wednesday Thursday Friday ] 9 18 100 }
+ ; one who has a job: two evenings at full use, and the weekend mornings at half
+ Configure.Span.{ [ Tuesday Thursday ] 19 23 100 }
+ Configure.Span.{ [ Saturday Sunday ] 9 13 50 }
+ ; a gradient: the hours around noon at full use, the early morning and the evening at less
+ Configure.Span.{ [ Monday Tuesday Wednesday Thursday Friday Saturday Sunday ] 6 10 60 }
+ Configure.Span.{ [ Monday Tuesday Wednesday Thursday Friday Saturday Sunday ] 10 14 100 }
+ Configure.Span.{ [ Monday Tuesday Wednesday Thursday Friday Saturday Sunday ] 14 22 70 }
+ ; an override: an afternoon at the dentist, two hours at nothing
+ Configure.Override.{ 1794859200 1794866400 0 }
```

```datom
  Configure.Target.{ Codex SpendBy.1762450320 }   ; use the week up before the reset expires
  Configure.Target.{ Claude Even }
  Read.Codex
  Read.{ { Codex true [ { Week 92 1762235580 10080 } ] [ { rc_1 Available 1762450320 } ] 1762210000 }
-        { Codex SpendBy.1762450320 88 92 Over 4 } }
+        { Codex SpendBy.1762450320 88 92 Over 48 32.0 0.25 } }
```

```datom
  energy-nexus 'Read.Codex'
  Read.{ { Codex true [ { Week 92 1762235580 10080 } ] [ { rc_1 Available 1762450320 } ] 1762210000 }
-        { Codex Even 23 92 Over 1 } }
+        { Codex Even 23 92 Over 120 80.0 0.1 } }
```

### Proposal 2: The type of a configuration is as wide as the people who set it · psyche-belief › intent/configuration.md, at its end

::: comment
His words, on the word and the placement: «Yeah, usefulness is good.» «intent modules are meant for system prompt.» And: «Whenever we design software, any kind of behavior that can be configurable must be configurable.» «giving examples is maybe a good way to give it more emphasis.» The first draft of this page obeyed the module in its values and broke it in its types: two numbers were configurable, and the shape of a person's week was fixed. The module names values and decisions; it does not yet say that a type can hardwire. The example is the one that failed, given as one of many.
:::

+ A type hardwires as surely as a literal: what the configuration's type cannot say, no one can set. A configuration is designed for the person least like its first user, and its type is as wide as their lives are different.

```ethos
+ ; one example of many: a schedule
+ Span.{ Vector<Weekday>               ; any hours of any days,
+        From.Hour To.Hour             ;   each at its own usefulness,
+        Usefulness }                  ;   so every week is sayable
```

## Questions

1. The one who has authority over a thinking machine needs a name of his own, the living being any living. The Nexus vision already says «owner»; this page uses it. Is owner the name?
