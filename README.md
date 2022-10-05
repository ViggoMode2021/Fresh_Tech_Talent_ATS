Applicant tracking systems can be both a blessing and a curse. They automate a lot of the résumé selection for job positions, however, they are known to be picky with applicants that might not have 'industry experience' in a field. For software developers who have attended bootcamps, they can often get 'auto-rejected' by ATS, even though they are entirely capable of at least being granted an interview.

Fresh Tech Talent ATS is the first applicant tracking system for SDE positions that selects applicants who have attended coding bootcamps. It is serverless and AWS native.

Here is the architecture in a nutshell:

1. Applicant applies for a job by uploading their résumé to the job posting. This sends the résumé to an S3 bucket.

2. The S3 bucket triggers a Lambda function (Python) that is using AWS Textract via the Boto3 SDK. Textract extracts the applicant's name, location, and email, as well as carefully checking if the applicant has attended a coding bootcamp. It will also look for key words like 'Python', 'JavaScript' etc. This is implemented primarily with Regex (Python 're' module). The applicant's information is then sent to a DynamoDB table with the time/date stamp as the primary key.

3. If the applicant has attended a bootcamp and has the required skills listed, then the applicant will receive an email sent by SES stating that they will be moving forward to an interview. If they have not attended a bootcamp, nor do they have the required skills listed, they will receive an email sent by SES stating that they will not be moving forward to an interview.

I hope to create a frontend for this project and maybe deploy it to test with a UI. For now, I've just been working on it in the AWS console.

I also want to give a huge shoutout to Srce Cde and for his Textract YouTube tutorial! It helped lay the beginning portion of the Lambda function and taught me quite a bit about the service.
