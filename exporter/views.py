import csv
import os
import shutil
from shutil import copyfile

import bagit
import boto3
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView

from concordia.models import Campaign, Transcription, UserAssetTagCollection


class ExportCampaignToCSV(TemplateView):
    """
    Exports the transcription and tags to csv file

    """

    template_name = "transcriptions/campaign.html"

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(slug=self.args[0])
        asset_list = campaign.asset_set.all().order_by("title", "sequence")
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="{0}.csv"'.format(
            campaign.slug
        )
        field_names = ["title", "description", "media_url"]
        writer = csv.writer(response)
        writer.writerow(
            ["Campaign", "Title", "Description", "MediaUrl", "Transcription", "Tags"]
        )
        for asset in asset_list:
            transcription = Transcription.objects.filter(
                asset=asset, user_id=self.request.user.id
            )
            if transcription:
                transcription = transcription[0].text
            else:
                transcription = ""
            tags = UserAssetTagCollection.objects.filter(
                asset=asset, user_id=self.request.user.id
            )
            if tags:
                tags = list(tags[0].tags.all().values_list("name", flat=True))
            else:
                tags = ""
            row = (
                [campaign.title]
                + [getattr(asset, i) for i in field_names]
                + [transcription, tags]
            )
            writer.writerow(row)
        return response


class ExportCampaignToBagit(TemplateView):
    """
    Creates temp directory structure for source data.  Copies source image
    file from S3 or local storage into temp directory, builds export.csv
    with meta, transcription, and tag data.  Executes bagit.py to turn temp
    directory into bagit strucutre.  Builds and exports bagit structure as
    zip.  Removes all temporary directories and files.

    """

    include_images = True
    template_name = "transcriptions/campaign.html"

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(slug=self.args[0])
        asset_list = campaign.asset_set.all().order_by("title", "sequence")

        # Make sure export folder exists (media/exporter)
        export_folder = "%s/exporter" % (settings.MEDIA_ROOT)
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Create temp exporter folder structure in media for bagit
        campaign_folder = "%s/exporter/%s" % (settings.MEDIA_ROOT, campaign.slug)

        # Create campaign folder (media/exporter/<campaign>)
        if not os.path.exists(campaign_folder):
            os.mkdir(campaign_folder)

        for asset in asset_list:
            item_folder_name = asset.media_url.rsplit("/")[-2]
            item_folder = "%s/%s" % (campaign_folder, item_folder_name)

            # Create asset folders (media/exporter/<campaign>/<asset>
            if not os.path.exists(item_folder):
                os.mkdir(item_folder)

            src_folder = item_folder.replace("exporter/", "")
            src_name = asset.media_url.rsplit("/")[-1]
            src_root = src_name.rsplit(".")[0]
            dest = "%s/%s" % (item_folder, src_name)

            if self.include_images:
                if campaign.s3_storage:
                    s3 = boto3.client(
                        "s3",
                        aws_access_key_id=settings.AWS_S3["AWS_ACCESS_KEY_ID"],
                        aws_secret_access_key=settings.AWS_S3["AWS_SECRET_ACCESS_KEY"],
                    )
                    bucket_name = settings.AWS_S3["S3_COLLECTION_BUCKET"]
                    s3_path = "{0}/{1}/{2}".format(
                        campaign.slug, item_folder_name, src_name
                    )
                    # Copy asset image from S3 into temp asset folder
                    s3.download_file(bucket_name, s3_path, dest)
                else:
                    src = "%s/%s" % (src_folder, src_name)
                    # Copy asset image from local storage into temp asset folder
                    copyfile(src, dest)

            # Get transcription data
            transcription_obj = Transcription.objects.filter(
                asset=asset, user_id=self.request.user.id
            )
            if transcription_obj:
                transcription = transcription_obj[0].text
            else:
                transcription = ""

            # Build transcription output text file
            tran_output_path = "{0}/{1}.txt".format(item_folder, src_root)
            tran_out_file = open(tran_output_path, "w")
            tran_out_file.write(transcription)
            tran_out_file.close()

        # Turn Structure into bagit format
        bagit.make_bag(campaign_folder, {"Contact-Name": request.user.username})

        # Build .zipfile of bagit formatted Campaign Folder
        archive_name = campaign_folder
        shutil.make_archive(archive_name, "zip", campaign_folder)

        # Download zip
        with open("%s.zip" % campaign_folder, "rb") as file:
            outfile = file.read()
        response = HttpResponse(outfile, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=%s.zip" % campaign.slug

        # Clean up temp folders & zipfile once exported
        try:
            shutil.rmtree(campaign_folder)
        except Exception as e:
            pass
        try:
            os.remove("%s.zip" % campaign_folder)
        except Exception as e:
            pass

        return response
