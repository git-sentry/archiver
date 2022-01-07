import {message, danger} from "danger"

const modifiedMD = FileReader.readAsText("output.txt")
message("Diffs applied by this PR: \n - " + modifiedMD)