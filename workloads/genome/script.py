from minio import Minio
from minio.error import S3Error
from datetime import datetime


import subprocess

def run_fastqc(fastq_file):
    """Runs FastQC on a FASTQ file.

    Args:
        fastq_file: The path to the FASTQ file.

    Returns:
        A tuple of the return code and the output of the FastQC command.
    """

    command = ["fastqc", fastq_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    return_code = process.wait()
    output = process.stdout.read().decode("utf-8")
    return return_code, output

def main():
    # Get the path to the FASTQ file.
    fastq_file = "/app/sample_data.fastq"

    # Run FastQC on the FASTQ file.
    return_code, output = run_fastqc(fastq_file)

    # Check the return code.
    if return_code != 0:
        raise Exception("FastQC failed with return code {}".format(return_code))

    # Save the output of FastQC.
    with open("fastqc_output.html", "w") as f:
        f.write(output)

    minio_client = Minio(
    '10.151.15.78:31252',
    access_key='Mq6wmeNk0NOc0vD9Efut',
    secret_key='Z3ETBqC3GuIiU9PomjBbmmC5h8I5I7WgN1wNWlCG',
    secure=False  # Set to True if using HTTPS
    )

    # Define the bucket and object name
    bucket_name = 'genome'
    file_name  = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Path to the file you want to upload
    file_path = '/app/sample_data_fastqc.html'

    # Upload the file
    try:
        # Ensure the bucket exists, if not, create it
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        # Upload the file
        minio_client.fput_object(
            bucket_name,
            file_name,
            file_path
        )
        print(f'File {file_name} uploaded successfully to {bucket_name}')
    except S3Error as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    main()