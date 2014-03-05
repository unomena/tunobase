'''
Created on 24 Feb 2014

@author: michael
'''
from django.test import TestCase
from django.contrib.sites.models import Site

from tunobase.corporate.company_info import models as company_info_models


class TeamModelTestCase(TestCase):
    """Set up the team model test cases."""

    def setUp(self):
        """Create Team Member Models"""
        self.team_member_position = company_info_models.CompanyMemberPosition\
            .objects.create(
                title='Team',
            )
        self.team_member_position.sites.add(Site.objects.get_current())

        self.investor_position = company_info_models.CompanyMemberPosition\
            .objects.create(
                title='Investors',
            )
        self.investor_position.sites.add(Site.objects.get_current())

        self.team_member = company_info_models.CompanyMember.objects.create(
            title='Team Member',
            job_title='Test Team Member'
        )
        self.team_member.positions.add(self.team_member_position)

        self.investor = company_info_models.CompanyMember.objects.create(
            title='Investor',
            job_title='Test Investor'
        )
        self.investor.positions.add(self.investor_position)

    def test_team_member_models(self):
        """
        Test that the Team Member Models were created with the
        correct positions

        """
        team_member_object = company_info_models.CompanyMember.objects.get(
            title='Team Member'
        )
        self.assertEqual(team_member_object, self.team_member)
        self.assertIn(
            self.team_member_position,
            team_member_object.positions.all()
        )

        investor_object = company_info_models.CompanyMember.objects.get(
            title='Investor'
        )
        self.assertEqual(investor_object, self.investor)
        self.assertIn(
            self.investor_position,
            investor_object.positions.all()
        )
