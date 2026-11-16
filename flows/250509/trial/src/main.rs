use std::{env, fs, process::ExitCode};
use typed_call_trial::{
    JudgingQueue, ModelCall, Operable, Processor, Promptable, Question, Submitting,
};

fn main() -> ExitCode {
    let arguments: Vec<String> = env::args().collect();
    let run = || -> Result<(), String> {
        if arguments.len() != 4 {
            return Err(
                "expected: prepare CALL.json PROMPT.txt, or invoke CALL.json PROCESSOR.json".into(),
            );
        }
        let call: ModelCall =
            serde_json::from_slice(&fs::read(&arguments[2]).map_err(|error| error.to_string())?)
                .map_err(|error| error.to_string())?;
        match arguments[1].as_str() {
            "prepare" => {
                if call.prompt_file != std::path::Path::new(&arguments[3]) {
                    return Err("prompt path must equal the typed call path".into());
                }
                fs::write(&call.prompt_file, call.question.prompt(&call.instruction)?)
                    .map_err(|error| error.to_string())?;
            }
            "invoke" => {
                let processor: Processor = serde_json::from_slice(
                    &fs::read(&arguments[3]).map_err(|error| error.to_string())?,
                )
                .map_err(|error| error.to_string())?;
                let observation = match &call.question {
                    Question::Admission { snapshot, .. } => Submitting {
                        expected_revision: snapshot.revision.clone(),
                        call,
                    }
                    .operate(&processor),
                    Question::Queue { .. } => JudgingQueue { call }.operate(&processor),
                };
                println!(
                    "{}",
                    serde_json::to_string_pretty(&observation).map_err(|error| error.to_string())?
                );
            }
            _ => return Err("unknown operation".into()),
        }
        Ok(())
    };
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("{error}");
            ExitCode::FAILURE
        }
    }
}
