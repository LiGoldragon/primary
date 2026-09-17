# Flow identity

## The process that starts a flow passes the Flow ID into the prompt, with the files and directories already created; the harness started in its own special place with its Flow ID in a file there, git-ignored, unwritable or soft-fenced; every subflow running that harness finds its own Flow ID easily or is told, starting its prompt with it; a subflow knows its Flow ID by the harness or a hook; Flow makes sense as the owner, though a flow would not usually have meta access to Flow; today there is no boundary there, only the models' guidance to be careful

Context: typed to the primary Claude f55ec8 on 2026-09-16 after the messaging spec book, asking why the flow itself runs the flow-id CLI; the question is answered in the reply. Logged by the main flow before acting.

> And why are we making the flow run the Flow ID CLI? Can't we get the process that starts the flow to get the ID passed into the prompt, like already with the files I already created, the directories, and the Flow ID in the log, or no, right? We're using the transcript now, or we should be using a simple sub-agent that already knows automatically its Flow ID by some miracle of the harness or hook or something.
>
> Maybe the harness is just started in its own special place, and it has its Flow ID in a file, even there in a Git-ignored file or something that it can't write to, or there's a soft fence there to not change that. All the subflows that are running that harness know they can find their own Flow ID easily, or they're told somehow they don't even need to. They start their prompt with it.
> ...
> Anyway, I think the Flow makes sense. It's just that you wouldn't have meta access to Flow usually, although right now there's no boundary there. It's just through guidance of the models to be careful.

-- psyche, typed.
